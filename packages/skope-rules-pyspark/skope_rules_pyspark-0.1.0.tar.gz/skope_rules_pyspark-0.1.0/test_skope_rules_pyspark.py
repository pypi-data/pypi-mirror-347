from __future__ import annotations

import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, IntegerType
from skope_rules_pyspark import SkopeRulesPySpark

@pytest.fixture(scope="session")
def spark() -> SparkSession:
    return SparkSession.builder \
        .appName("SkopeRulesPySparkTest") \
        .master("local[2]") \
        .getOrCreate()

@pytest.fixture
def sample_data(spark: SparkSession):
    schema = StructType([
        StructField("feature1", DoubleType(), True),
        StructField("feature2", DoubleType(), True),
        StructField("feature3", DoubleType(), True),
        StructField("label", IntegerType(), True)
    ])
    
    data = [
        (1.0, 2.0, 3.0, 1),  # Positive example
        (1.0, 2.0, 1.0, 1),  # Positive example
        (4.0, 5.0, 6.0, 0),  # Negative example
        (4.0, 2.0, 3.0, 0),  # Negative example
        (1.0, 5.0, 3.0, 1),  # Positive example
        (4.0, 5.0, 1.0, 0),  # Negative example
    ]
    
    return spark.createDataFrame(data, schema)

def test_skope_rules_fit_transform(spark: SparkSession, sample_data):
    # Initialize SkopeRulesPySpark
    skope = SkopeRulesPySpark(
        feature_names=["feature1", "feature2", "feature3"],
        precision_min=0.5,
        recall_min=0.1,
        n_estimators=2,
        max_depth=2
    )
    
    # Fit the model
    skope.fit(sample_data)
    
    # Get rules
    rules = skope.get_rules()
    assert len(rules) > 0, "No rules were generated"
    
    # Transform data
    transformed_df = skope.transform(sample_data)
    
    # Check if prediction column exists
    assert "prediction" in transformed_df.columns, "Prediction column not found"
    
    # Check if predictions are binary
    predictions = transformed_df.select("prediction").distinct().collect()
    prediction_values = [row.prediction for row in predictions]
    assert all(p in [0, 1] for p in prediction_values), "Predictions are not binary"

def test_skope_rules_predict(spark: SparkSession, sample_data):
    skope = SkopeRulesPySpark(
        feature_names=["feature1", "feature2", "feature3"],
        precision_min=0.5,
        recall_min=0.1,
        n_estimators=2,
        max_depth=2
    )
    
    skope.fit(sample_data)
    
    # Test predict method
    predictions_df = skope.predict(sample_data)
    assert "prediction" in predictions_df.columns, "Prediction column not found"
    assert predictions_df.count() == sample_data.count(), "Number of predictions doesn't match input data"

def test_skope_rules_rule_evaluation(spark: SparkSession, sample_data):
    skope = SkopeRulesPySpark(
        feature_names=["feature1", "feature2", "feature3"],
        precision_min=0.7,  # Higher precision threshold
        recall_min=0.3,     # Higher recall threshold
        n_estimators=2,
        max_depth=2
    )
    
    skope.fit(sample_data)
    rules = skope.get_rules()
    
    # Check if rules meet precision and recall thresholds
    for rule, (precision, recall, _) in rules.items():
        assert precision >= 0.7, f"Rule {rule} has precision {precision} below threshold 0.7"
        assert recall >= 0.3, f"Rule {rule} has recall {recall} below threshold 0.3"

def test_skope_rules_feature_names(spark: SparkSession, sample_data):
    # Test without specifying feature names
    skope = SkopeRulesPySpark(
        precision_min=0.5,
        recall_min=0.1,
        n_estimators=2,
        max_depth=2
    )
    
    skope.fit(sample_data)
    assert skope.feature_names == ["feature1", "feature2", "feature3"], "Feature names not correctly inferred" 