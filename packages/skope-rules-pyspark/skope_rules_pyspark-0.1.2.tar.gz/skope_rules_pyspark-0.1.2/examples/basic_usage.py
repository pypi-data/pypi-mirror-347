from __future__ import annotations

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, IntegerType
from skope_rules_pyspark import SkopeRulesPySpark

def main():
    spark = SparkSession.builder \
        .appName("SkopeRulesPySparkExample") \
        .master("local[2]") \
        .getOrCreate()

    # Classification example
    print("\n=== Classification Example ===")
    schema = StructType([
        StructField("feature1", DoubleType(), True),
        StructField("feature2", DoubleType(), True),
        StructField("feature3", DoubleType(), True),
        StructField("label", IntegerType(), True),
        StructField("weight", DoubleType(), True)
    ])

    data = [
        (1.0, 2.0, 3.0, 1, 1.0),
        (1.0, 2.0, 1.0, 1, 2.0),
        (4.0, 5.0, 6.0, 0, 1.0),
        (4.0, 2.0, 3.0, 0, 1.0),
        (1.0, 5.0, 3.0, 1, 1.0),
        (4.0, 5.0, 1.0, 0, 1.0),
    ]

    df = spark.createDataFrame(data, schema)

    skope = SkopeRulesPySpark(
        feature_names=["feature1", "feature2", "feature3"],
        precision_min=0.5,
        recall_min=0.1,
        n_estimators=2,
        max_depth=2,
        sample_weight_col="weight",
        bootstrap=True
    )

    skope.fit(df)
    
    print("\nRègles générées :")
    rules = skope.get_rules()
    for rule, (precision, recall, nb) in rules.items():
        print(f"{rule} | precision={precision:.2f} | recall={recall:.2f} | nb={nb}")

    print("\nMeilleures règles :")
    best_rules = skope.get_best_rules(n_rules=2)
    for rule, (precision, recall, nb) in best_rules:
        print(f"{rule} | precision={precision:.2f} | recall={recall:.2f} | nb={nb}")

    print("\nImportance des features :")
    importances = skope.get_feature_importances()
    for feature, importance in importances.items():
        print(f"{feature}: {importance:.3f}")

    print("\nÉvaluation des règles :")
    eval_df = skope.evaluate_rules(df)
    eval_df.show()

    print("\nPrédictions :")
    predictions = skope.predict(df)
    predictions.show()

    print("\nScores de vote :")
    vote_scores = skope.rules_vote(df)
    vote_scores.show()

    # Regression example
    print("\n=== Regression Example ===")
    reg_schema = StructType([
        StructField("feature1", DoubleType(), True),
        StructField("feature2", DoubleType(), True),
        StructField("feature3", DoubleType(), True),
        StructField("label", DoubleType(), True),
        StructField("weight", DoubleType(), True)
    ])

    reg_data = [
        (1.0, 2.0, 3.0, 10.0, 1.0),
        (1.0, 2.0, 1.0, 8.0, 2.0),
        (4.0, 5.0, 6.0, 15.0, 1.0),
        (4.0, 2.0, 3.0, 12.0, 1.0),
        (1.0, 5.0, 3.0, 9.0, 1.0),
        (4.0, 5.0, 1.0, 14.0, 1.0),
    ]

    reg_df = spark.createDataFrame(reg_data, reg_schema)

    reg_skope = SkopeRulesPySpark(
        feature_names=["feature1", "feature2", "feature3"],
        precision_min=0.5,
        recall_min=0.1,
        n_estimators=2,
        max_depth=2,
        task="regression",
        sample_weight_col="weight"
    )

    reg_skope.fit(reg_df)
    
    print("\nRègles de régression générées :")
    reg_rules = reg_skope.get_rules()
    for rule, (r2, coverage, nb) in reg_rules.items():
        print(f"{rule} | R²={r2:.2f} | coverage={coverage:.2f} | nb={nb}")

    print("\nÉvaluation des règles de régression :")
    reg_eval_df = reg_skope.evaluate_rules(reg_df)
    reg_eval_df.show()

    print("\nPrédictions de régression :")
    reg_predictions = reg_skope.predict(reg_df)
    reg_predictions.show()

    spark.stop()

if __name__ == "__main__":
    main() 