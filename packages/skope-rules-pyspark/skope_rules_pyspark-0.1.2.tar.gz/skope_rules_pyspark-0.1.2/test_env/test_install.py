from pyspark.sql import SparkSession
from skope_rules_pyspark import SkopeRulesPySpark

# Créer une session Spark
spark = SparkSession.builder \
    .appName("TestSkopeRules") \
    .master("local[2]") \
    .getOrCreate()

# Créer un DataFrame de test
data = [
    (1.0, 2.0, 3.0, 1),
    (1.0, 2.0, 1.0, 1),
    (4.0, 5.0, 6.0, 0),
    (4.0, 2.0, 3.0, 0),
    (1.0, 5.0, 3.0, 1),
    (4.0, 5.0, 1.0, 0),
]

df = spark.createDataFrame(data, ["feature1", "feature2", "feature3", "label"])

# Initialiser et entraîner le modèle
skope = SkopeRulesPySpark(
    feature_names=["feature1", "feature2", "feature3"],
    precision_min=0.5,
    recall_min=0.1,
    n_estimators=2,
    max_depth=2
)

skope.fit(df)

# Afficher les règles générées
print("\nRègles générées :")
for rule, (precision, recall, nb) in skope.get_rules().items():
    print(f"Règle : {rule}")
    print(f"Précision : {precision:.2f}")
    print(f"Rappel : {recall:.2f}")
    print(f"Support : {nb}")
    print()

# Faire des prédictions
predictions = skope.predict(df)
print("\nPrédictions :")
predictions.show()

print("\nTest terminé avec succès : le package fonctionne.") 