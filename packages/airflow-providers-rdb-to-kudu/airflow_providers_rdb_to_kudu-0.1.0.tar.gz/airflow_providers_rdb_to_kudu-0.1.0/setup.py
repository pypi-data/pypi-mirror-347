from setuptools import find_packages, setup

setup(
    name="airflow-providers-rdb-to-kudu",
    version="0.1.0",
    author="Archer Yang",
    author_email="archer.yang@crypto.com",
    description="A custom Airflow operator to upsert data from RDB to Kudu.",
    packages=find_packages(),
    install_requires=["kudu-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Apache Airflow",
        "License :: OSI Approved :: MIT License",
    ],
)
