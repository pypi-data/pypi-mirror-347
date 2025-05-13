from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, expr, lit, when, sum as spark_sum, count, mean, variance, stddev
from pyspark.sql.types import DoubleType, IntegerType, StructField, StructType
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.regression import DecisionTreeRegressor
import numpy as np
import re
from collections import Counter

class SkopeRulesPySpark:
    def __init__(
        self,
        feature_names: list[str] | None = None,
        precision_min: float = 0.5,
        recall_min: float = 0.01,
        n_estimators: int = 10,
        max_depth: int = 3,
        max_features: int | float | str = 1.0,
        min_samples_split: int = 2,
        random_state: int | None = None,
        max_depth_duplication: int | None = None,
        sample_weight_col: str | None = None,
        task: str = "classification",
        max_samples: float = 0.8,
        bootstrap: bool = False
    ) -> None:
        self.feature_names = feature_names
        self.precision_min = precision_min
        self.recall_min = recall_min
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        self.max_depth_duplication = max_depth_duplication
        self.sample_weight_col = sample_weight_col
        self.task = task
        self.max_samples = max_samples
        self.bootstrap = bootstrap
        self.rules_: dict[str, tuple[float, float, int]] = {}
        self.estimators_: list[PipelineModel] = []
        self.feature_importances_: dict[str, float] = {}

    def _create_pipeline(self, features_col: str) -> Pipeline:
        assembler = VectorAssembler(
            inputCols=self.feature_names,
            outputCol=features_col
        )
        
        if self.task == "classification":
            model = DecisionTreeClassifier(
                featuresCol=features_col,
                labelCol="label",
                maxDepth=self.max_depth,
                minInstancesPerNode=self.min_samples_split,
                maxBins=32,
                seed=self.random_state
            )
        else:  # regression
            model = DecisionTreeRegressor(
                featuresCol=features_col,
                labelCol="label",
                maxDepth=self.max_depth,
                minInstancesPerNode=self.min_samples_split,
                maxBins=32,
                seed=self.random_state
            )
            
        return Pipeline(stages=[assembler, model])

    def _replace_feature_indices(self, cond: str, feature_names: list[str]) -> str:
        def repl(m):
            idx = int(m.group(1))
            return feature_names[idx]
        return re.sub(r"feature (\d+)", repl, cond)

    def _extract_rules_from_tree(self, tree_model: Any, feature_names: list[str]) -> list[str]:
        debug_str = tree_model.toDebugString
        lines = debug_str.split("\n")
        rules = []
        path = []
        for line in lines[1:]:
            indent = len(line) - len(line.lstrip())
            content = line.strip()
            while path and path[-1][0] >= indent:
                path.pop()
            if "If (" in content or "Else (" in content:
                cond = content.split("(", 1)[1].rsplit(")", 1)[0]
                cond = self._replace_feature_indices(cond, feature_names)
                path.append((indent, cond))
            if self.task == "classification":
                if "Predict: 1.0" in content:
                    rule = " and ".join(cond for _, cond in path)
                    rules.append(rule)
            else:  # regression
                if "Predict:" in content:
                    rule = " and ".join(cond for _, cond in path)
                    rules.append(rule)
        return rules

    def _prepare_sample_weights(self, df: DataFrame) -> DataFrame:
        if self.sample_weight_col:
            if self.bootstrap:
                # Normalize weights for bootstrap sampling
                total_weight = df.select(spark_sum(self.sample_weight_col)).collect()[0][0]
                return df.withColumn(
                    "normalized_weight",
                    col(self.sample_weight_col) / total_weight
                )
            return df
        return df.withColumn("normalized_weight", lit(1.0))

    def _evaluate_regression_rule(self, rule: str, df: DataFrame) -> tuple[float, float, int]:
        rule_df = df.withColumn("rule_pred", expr(rule))
        
        if self.sample_weight_col:
            stats = rule_df.filter(col("rule_pred") == 1).select(
                mean("label").alias("mean"),
                stddev("label").alias("stddev"),
                spark_sum(self.sample_weight_col).alias("weight_sum")
            ).collect()[0]
            weight_sum = stats["weight_sum"] if stats["weight_sum"] is not None else 0
            if weight_sum == 0:
                return 0.0, 0.0, 0
            total_variance = df.select(variance("label")).collect()[0][0]
            explained_variance = (stats["stddev"] or 0) ** 2
            r2_score = 1 - (explained_variance / total_variance) if total_variance > 0 else 0
            coverage = weight_sum / df.select(spark_sum(self.sample_weight_col)).collect()[0][0]
            return r2_score, coverage, int(weight_sum)
        else:
            stats = rule_df.filter(col("rule_pred") == 1).select(
                mean("label").alias("mean"),
                stddev("label").alias("stddev"),
                count("*").alias("count")
            ).collect()[0]
            count_val = stats["count"] if stats["count"] is not None else 0
            if count_val == 0:
                return 0.0, 0.0, 0
            total_variance = df.select(variance("label")).collect()[0][0]
            explained_variance = (stats["stddev"] or 0) ** 2
            r2_score = 1 - (explained_variance / total_variance) if total_variance > 0 else 0
            coverage = count_val / df.count()
            return r2_score, coverage, count_val

    def _evaluate_rule(self, rule: str, df: DataFrame) -> tuple[float, float, int]:
        if self.task == "regression":
            return self._evaluate_regression_rule(rule, df)
        rule_df = df.withColumn("rule_pred", expr(rule))
        if self.sample_weight_col:
            total = df.select(spark_sum(self.sample_weight_col)).collect()[0][0]
            true_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 1)) \
                .select(spark_sum(self.sample_weight_col)).collect()[0][0]
            false_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 0)) \
                .select(spark_sum(self.sample_weight_col)).collect()[0][0]
            true_positives = true_positives if true_positives is not None else 0
            false_positives = false_positives if false_positives is not None else 0
        else:
            total = df.count()
            true_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 1)).count()
            false_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 0)).count()
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / total if total > 0 else 0
        return precision, recall, true_positives

    def _update_feature_importances(self, tree_model: Any) -> None:
        importances = tree_model.featureImportances.toArray()
        for feature, importance in zip(self.feature_names, importances):
            self.feature_importances_[feature] = self.feature_importances_.get(feature, 0) + importance

    def fit(self, df: DataFrame) -> SkopeRulesPySpark:
        if self.feature_names is None:
            self.feature_names = [c for c in df.columns if c not in ["label", self.sample_weight_col]]
            
        if self.sample_weight_col and self.sample_weight_col not in df.columns:
            raise ValueError(f"Sample weight column {self.sample_weight_col} not found in DataFrame")
            
        df = self._prepare_sample_weights(df)
        
        for _ in range(self.n_estimators):
            pipeline = self._create_pipeline("features")
            model = pipeline.fit(df)
            self.estimators_.append(model)
            tree_model = model.stages[-1]
            
            self._update_feature_importances(tree_model)
            rules = self._extract_rules_from_tree(tree_model, self.feature_names)
            
            for rule in rules:
                precision, recall, nb = self._evaluate_rule(rule, df)
                if precision >= self.precision_min and recall >= self.recall_min:
                    self.rules_[rule] = (precision, recall, nb)
                    
        if self.max_depth_duplication is not None:
            self.rules_ = self.deduplicate(self.rules_)
            
        # Normalize feature importances
        total_importance = sum(self.feature_importances_.values())
        if total_importance > 0:
            self.feature_importances_ = {
                k: v / total_importance 
                for k, v in self.feature_importances_.items()
            }
            
        return self

    def transform(self, df: DataFrame) -> DataFrame:
        result_df = df
        rule_cols = []
        
        for i, rule in enumerate(self.rules_):
            col_name = f"rule_{i}"
            result_df = result_df.withColumn(
                col_name,
                expr(rule).cast(IntegerType())
            )
            rule_cols.append(col_name)
        
        sum_expr = " + ".join(rule_cols)
        result_df = result_df.withColumn(
            "prediction",
            expr(f"CASE WHEN ({sum_expr}) > 0 THEN 1 ELSE 0 END")
        )
        
        return result_df

    def predict(self, df: DataFrame) -> DataFrame:
        return self.transform(df).select("prediction")

    def rules_vote(self, df: DataFrame) -> DataFrame:
        result_df = df
        rule_cols = []
        
        for i, rule in enumerate(self.rules_):
            col_name = f"rule_{i}"
            result_df = result_df.withColumn(
                col_name,
                expr(rule).cast(IntegerType())
            )
            rule_cols.append(col_name)
        
        sum_expr = " + ".join(rule_cols)
        return result_df.withColumn("vote_score", expr(sum_expr))

    def score_top_rules(self, df: DataFrame) -> DataFrame:
        result_df = df
        for i, (rule, _) in enumerate(self.rules_):
            col_name = f"rule_{i}"
            result_df = result_df.withColumn(
                col_name,
                expr(rule).cast(IntegerType())
            )
            
        score_expr = "CASE " + " ".join([
            f"WHEN rule_{i} = 1 THEN {len(self.rules_) - i} " 
            for i in range(len(self.rules_))
        ]) + " ELSE 0 END"
        
        return result_df.withColumn("top_rules_score", expr(score_expr))

    def predict_top_rules(self, df: DataFrame, n_rules: int) -> DataFrame:
        scores_df = self.score_top_rules(df)
        return scores_df.withColumn(
            "prediction",
            expr(f"CASE WHEN top_rules_score > {len(self.rules_) - n_rules} THEN 1 ELSE 0 END")
        )

    def deduplicate(self, rules: dict[str, tuple[float, float, int]]) -> dict[str, tuple[float, float, int]]:
        def split_with_best_feature(rules_list: list[tuple[str, tuple[float, float, int]]], 
                                  depth: int, 
                                  exceptions: list[str] = None) -> list[list[tuple[str, tuple[float, float, int]]]]:
            if depth == 0 or not rules_list:
                return [rules_list]
                
            if exceptions is None:
                exceptions = []
                
            rulelist = [rule[0].split(' and ') for rule in rules_list]
            terms = [t.split(' ')[0] for term in rulelist for t in term]
            counter = Counter(terms)
            
            for exception in exceptions:
                if exception in counter:
                    del counter[exception]
                    
            if not counter:
                return [rules_list]
                
            most_represented_term = counter.most_common()[0][0]
            rules_splitted = [[], [], []]
            
            for rule in rules_list:
                if (most_represented_term + ' <=') in rule[0]:
                    rules_splitted[0].append(rule)
                elif (most_represented_term + ' >') in rule[0]:
                    rules_splitted[1].append(rule)
                else:
                    rules_splitted[2].append(rule)
                    
            new_exceptions = exceptions + [most_represented_term]
            return [split_with_best_feature(ruleset, depth-1, new_exceptions) 
                   for ruleset in rules_splitted if ruleset]

        def breadth_first_search(rules: list, leaves: list = None) -> list:
            if leaves is None:
                leaves = []
                
            if not rules or not isinstance(rules[0], list):
                if rules:
                    leaves.append(rules)
            else:
                for rules_child in rules:
                    breadth_first_search(rules_child, leaves)
            return leaves

        rules_list = list(rules.items())
        res = split_with_best_feature(rules_list, self.max_depth_duplication)
        leaves = []
        breadth_first_search(res, leaves)
        
        return {max(rules_set, key=lambda x: self.f1_score(x))[0]: max(rules_set, key=lambda x: self.f1_score(x))[1]
                for rules_set in leaves}

    def f1_score(self, x: tuple[str, tuple[float, float, int]]) -> float:
        precision, recall = x[1][0], x[1][1]
        return 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    def get_rules(self) -> dict[str, tuple[float, float, int]]:
        return self.rules_ 

    def get_feature_importances(self) -> dict[str, float]:
        return self.feature_importances_

    def evaluate_rules(self, df: DataFrame) -> DataFrame:
        results = []
        for rule, (precision, recall, _) in self.rules_.items():
            rule_df = df.withColumn("rule_pred", expr(rule))
            if self.task == "classification":
                if self.sample_weight_col:
                    total = df.select(spark_sum(self.sample_weight_col)).collect()[0][0]
                    true_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 1)) \
                        .select(spark_sum(self.sample_weight_col)).collect()[0][0]
                    false_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 0)) \
                        .select(spark_sum(self.sample_weight_col)).collect()[0][0]
                    true_positives = true_positives if true_positives is not None else 0
                    false_positives = false_positives if false_positives is not None else 0
                else:
                    total = df.count()
                    true_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 1)).count()
                    false_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 0)).count()
                precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
                recall = true_positives / total if total > 0 else 0
                f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
                results.append({
                    "rule": rule,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1,
                    "support": true_positives
                })
            else:  # regression
                stats = rule_df.filter(col("rule_pred") == 1).select(
                    mean("label").alias("mean"),
                    stddev("label").alias("stddev"),
                    count("*").alias("count")
                ).collect()[0]
                count_val = stats["count"] if stats["count"] is not None else 0
                if count_val > 0:
                    total_variance = df.select(variance("label")).collect()[0][0]
                    explained_variance = (stats["stddev"] or 0) ** 2
                    r2_score = 1 - (explained_variance / total_variance) if total_variance > 0 else 0
                    results.append({
                        "rule": rule,
                        "r2_score": r2_score,
                        "mean": stats["mean"],
                        "stddev": stats["stddev"],
                        "support": count_val
                    })
        return df.sparkSession.createDataFrame(results)

    def get_best_rules(self, n_rules: int = 5) -> list[tuple[str, tuple[float, float, int]]]:
        """Return the n best rules based on F1 score for classification or R² for regression."""
        if self.task == "classification":
            return sorted(
                self.rules_.items(),
                key=lambda x: self.f1_score(x),
                reverse=True
            )[:n_rules]
        else:
            return sorted(
                self.rules_.items(),
                key=lambda x: x[1][0],  # R² score
                reverse=True
            )[:n_rules] 