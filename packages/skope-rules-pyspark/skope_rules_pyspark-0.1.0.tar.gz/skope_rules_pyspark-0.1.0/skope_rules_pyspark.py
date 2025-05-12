from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, expr, lit, when
from pyspark.sql.types import DoubleType, IntegerType, StructField, StructType
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import numpy as np
import re

class SkopeRulesPySpark:
    def __init__(
        self,
        feature_names: List[str] | None = None,
        precision_min: float = 0.5,
        recall_min: float = 0.01,
        n_estimators: int = 10,
        max_depth: int = 3,
        max_features: Union[int, float, str] = 1.0,
        min_samples_split: int = 2,
        random_state: int | None = None
    ) -> None:
        self.feature_names = feature_names
        self.precision_min = precision_min
        self.recall_min = recall_min
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        self.rules_: Dict[str, tuple[float, float, int]] = {}
        self.estimators_: List[PipelineModel] = []
        
    def _create_pipeline(self, features_col: str) -> Pipeline:
        assembler = VectorAssembler(
            inputCols=self.feature_names,
            outputCol=features_col
        )
        
        dt = DecisionTreeClassifier(
            featuresCol=features_col,
            labelCol="label",
            maxDepth=self.max_depth,
            minInstancesPerNode=self.min_samples_split,
            maxBins=32,
            seed=self.random_state
        )
        
        return Pipeline(stages=[assembler, dt])
    
    def _replace_feature_indices(self, cond: str, feature_names: List[str]) -> str:
        def repl(m):
            idx = int(m.group(1))
            return feature_names[idx]
        return re.sub(r"feature (\d+)", repl, cond)
    
    def _extract_rules_from_tree(self, tree_model: Any, feature_names: List[str]) -> List[str]:
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
            if "Predict: 1.0" in content:
                rule = " and ".join(cond for _, cond in path)
                rules.append(rule)
        return rules
    
    def _evaluate_rule(self, rule: str, df: DataFrame) -> tuple[float, float, int]:
        rule_df = df.withColumn("rule_pred", expr(rule))
        total = df.count()
        true_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 1)).count()
        false_positives = rule_df.filter((col("rule_pred") == 1) & (col("label") == 0)).count()
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / total if total > 0 else 0
        
        return precision, recall, true_positives
    
    def fit(self, df: DataFrame) -> SkopeRulesPySpark:
        if self.feature_names is None:
            self.feature_names = [c for c in df.columns if c != "label"]
        
        for _ in range(self.n_estimators):
            pipeline = self._create_pipeline("features")
            model = pipeline.fit(df)
            self.estimators_.append(model)
            
            tree_model = model.stages[-1]
            rules = self._extract_rules_from_tree(tree_model, self.feature_names)
            
            for rule in rules:
                precision, recall, nb = self._evaluate_rule(rule, df)
                if precision >= self.precision_min and recall >= self.recall_min:
                    self.rules_[rule] = (precision, recall, nb)
        
        return self
    
    def transform(self, df: DataFrame) -> DataFrame:
        result_df = df
        
        for rule in self.rules_:
            result_df = result_df.withColumn(
                f"rule_{hash(rule)}",
                expr(rule).cast(IntegerType())
            )
        
        rule_cols = [f"rule_{hash(rule)}" for rule in self.rules_]
        result_df = result_df.withColumn(
            "prediction",
            when(sum(col(c) for c in rule_cols) > 0, 1).otherwise(0)
        )
        
        return result_df
    
    def predict(self, df: DataFrame) -> DataFrame:
        return self.transform(df).select("prediction")
    
    def get_rules(self) -> Dict[str, tuple[float, float, int]]:
        return self.rules_




