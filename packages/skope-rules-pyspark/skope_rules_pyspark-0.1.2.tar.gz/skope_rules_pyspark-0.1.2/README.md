# Skope Rules PySpark

Ce package fournit une implémentation de Skope Rules pour la classification binaire en utilisant PySpark. Il permet de générer des règles de décision à partir d'un ensemble de données d'entraînement.

## Installation

```sh
pip install skope-rules-pyspark
```

## Utilisation

### Exemple simple

```python
from pyspark.sql import SparkSession
from skope_rules_pyspark import SkopeRulesPySpark

# Initialiser une session Spark
spark = SparkSession.builder.appName("SkopeRulesExample").getOrCreate()

# Charger les données d'entraînement
train_data = spark.read.csv("path/to/train_data.csv", header=True, inferSchema=True)

# Initialiser et entraîner le modèle
model = SkopeRulesPySpark()
model.fit(train_data, target_col="target")

# Générer les règles
rules = model.generate_rules()
print(rules)
```

### Exemple complet

```python
from pyspark.sql import SparkSession
from skope_rules_pyspark import SkopeRulesPySpark

# Initialiser une session Spark
spark = SparkSession.builder.appName("SkopeRulesExample").getOrCreate()

# Charger les données d'entraînement
train_data = spark.read.csv("path/to/train_data.csv", header=True, inferSchema=True)

# Initialiser et entraîner le modèle
model = SkopeRulesPySpark()
model.fit(train_data, target_col="target")

# Générer les règles
rules = model.generate_rules()
print(rules)

# Prédire sur de nouvelles données
test_data = spark.read.csv("path/to/test_data.csv", header=True, inferSchema=True)
predictions = model.predict(test_data)
print(predictions)
```

## Fonctionnalités

- Génération de règles de décision pour la classification binaire
- Utilisation de PySpark pour le traitement de données à grande échelle
- Compatible avec les versions récentes de PySpark (>=3.0.0)

## Dépendances

- pyspark>=3.0.0
- numpy>=1.21.6

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Auteur

Mickael Assaraf - mickael.assaraf@gmail.com

## Liens

- [GitHub](https://github.com/mickaelassaraf/skope-rules-pyspark)
- [PyPI](https://pypi.org/project/skope-rules-pyspark/)

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