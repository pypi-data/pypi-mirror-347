# Skope Rules PySpark

Une implémentation PySpark de Skope Rules pour la classification binaire.

## Installation

```bash
pip install skope-rules-pyspark
```

## Utilisation

```python
from pyspark.sql import SparkSession
from skope_rules_pyspark import SkopeRulesPySpark

# Créer une session Spark
spark = SparkSession.builder \
    .appName("SkopeRulesPySparkExample") \
    .master("local[2]") \
    .getOrCreate()

# Créer un DataFrame d'exemple
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

# Obtenir les règles générées
rules = skope.get_rules()
for rule, (precision, recall, nb) in rules.items():
    print(f"{rule} | precision={precision:.2f} | recall={recall:.2f} | nb={nb}")

# Faire des prédictions
predictions = skope.predict(df)
predictions.show()
```

## Paramètres

- `feature_names` : Liste des noms des colonnes à utiliser comme features
- `precision_min` : Précision minimale requise pour une règle (défaut: 0.5)
- `recall_min` : Rappel minimal requis pour une règle (défaut: 0.01)
- `n_estimators` : Nombre d'arbres de décision à entraîner (défaut: 10)
- `max_depth` : Profondeur maximale des arbres (défaut: 3)
- `max_features` : Nombre maximum de features à considérer (défaut: 1.0)
- `min_samples_split` : Nombre minimum d'échantillons requis pour diviser un nœud (défaut: 2)
- `random_state` : Seed pour la reproductibilité (défaut: None)

## Méthodes

- `fit(df)` : Entraîne le modèle sur un DataFrame PySpark
- `predict(df)` : Retourne les prédictions pour un DataFrame
- `transform(df)` : Applique les règles et retourne le DataFrame avec les prédictions
- `get_rules()` : Retourne les règles générées avec leurs métriques

## Développement

1. Cloner le repository
2. Installer les dépendances de développement :
   ```bash
   pip install -e ".[dev]"
   ```
3. Lancer les tests :
   ```bash
   pytest tests/
   ```

## Licence

MIT 