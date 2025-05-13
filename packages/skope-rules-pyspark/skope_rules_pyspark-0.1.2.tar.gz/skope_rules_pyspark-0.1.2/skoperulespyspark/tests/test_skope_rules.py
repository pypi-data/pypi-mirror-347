from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType
from skope_rules_pyspark import SkopeRulesPySpark

def test_regression():
    spark = SparkSession.builder \
        .appName("SkopeRulesPySparkTest") \
        .master("local[2]") \
        .getOrCreate()

    schema = StructType([
        StructField("feature1", DoubleType(), True),
        StructField("feature2", DoubleType(), True),
        StructField("feature3", DoubleType(), True),
        StructField("label", DoubleType(), True),
        StructField("weight", DoubleType(), True)
    ])

    data = [
        (1.0, 2.0, 3.0, 10.0, 1.0),
        (1.0, 2.0, 1.0, 8.0, 2.0),
        (4.0, 5.0, 6.0, 15.0, 1.0),
        (4.0, 2.0, 3.0, 12.0, 1.0),
        (1.0, 5.0, 3.0, 9.0, 1.0),
        (4.0, 5.0, 1.0, 14.0, 1.0),
    ]

    df = spark.createDataFrame(data, schema)

    # Test regression avec seuils permissifs
    skope = SkopeRulesPySpark(
        feature_names=["feature1", "feature2", "feature3"],
        precision_min=0.0,
        recall_min=0.0,
        n_estimators=2,
        max_depth=2,
        task="regression",
        sample_weight_col="weight"
    )

    skope.fit(df)
    rules = skope.get_rules()
    assert len(rules) > 0, "No rules were generated"

    # Test predictions
    predictions = skope.predict(df)
    assert predictions.count() == df.count(), "Number of predictions doesn't match input data"
    assert "prediction" in predictions.columns, "Prediction column is missing"

    # Test rule evaluation
    eval_df = skope.evaluate_rules(df)
    assert "r2_score" in eval_df.columns, "R² score missing"
    assert "mean" in eval_df.columns, "Mean missing"
    assert "stddev" in eval_df.columns, "Standard deviation missing"

    spark.stop() 