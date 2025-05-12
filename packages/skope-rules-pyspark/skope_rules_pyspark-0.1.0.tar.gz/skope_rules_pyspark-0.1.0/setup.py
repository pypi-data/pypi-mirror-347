from setuptools import setup, find_packages

setup(
    name="skope-rules-pyspark",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyspark==3.0.0",
        "pytest==7.4.3",
        "numpy==1.21.6",
    ],
) 