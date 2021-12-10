from pyspark.sql import SparkSession


spark = SparkSession.builder.appName('Zeppelin-Interpreter').master('yarn').getOrCreate()
