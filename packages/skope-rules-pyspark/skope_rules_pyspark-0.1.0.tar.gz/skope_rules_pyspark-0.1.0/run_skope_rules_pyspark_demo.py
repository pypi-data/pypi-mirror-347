from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, IntegerType
from skope_rules_pyspark import SkopeRulesPySpark

spark = SparkSession.builder \
    .appName("SkopeRulesPySparkDemo") \
    .master("local[2]") \
    .getOrCreate()

schema = StructType([
    StructField("feature1", DoubleType(), True),
    StructField("feature2", DoubleType(), True),
    StructField("feature3", DoubleType(), True),
    StructField("label", IntegerType(), True)
])

data = [
    (1.0, 2.0, 3.0, 1),
    (1.0, 2.0, 1.0, 1),
    (4.0, 5.0, 6.0, 0),
    (4.0, 2.0, 3.0, 0),
    (1.0, 5.0, 3.0, 1),
    (4.0, 5.0, 1.0, 0),
]

df = spark.createDataFrame(data, schema)

skope = SkopeRulesPySpark(
    feature_names=["feature1", "feature2", "feature3"],
    precision_min=0.5,
    recall_min=0.1,
    n_estimators=2,
    max_depth=2
)

skope.fit(df)
rules = skope.get_rules()
print("Règles générées :")
for rule, (precision, recall, nb) in rules.items():
    print(f"{rule} | precision={precision:.2f} | recall={recall:.2f} | nb={nb}")

predictions = skope.predict(df)
print("\nPrédictions :")
predictions.show() 