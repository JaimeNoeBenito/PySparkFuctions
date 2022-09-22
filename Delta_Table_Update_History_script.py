# Databricks notebook source
# MAGIC %run your_import_functions_script

# COMMAND ----------

# Import the file with the correct values
_DATA_FILENAME= dbutils.widgets.get("_DATA_FILENAME")
print(_DATA_FILENAME)

# COMMAND ----------

from pyspark.sql import SQLContext
from pyspark.sql import HiveContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark import SparkContext, SparkConf
from pyspark.sql import DataFrame
from pyspark import StorageLevel
spark.conf.set("spark.sql.execution.arrow.enabled", "true") 
spark.sql("SET spark.sql.sources.commitProtocolClass=com.databricks.io.CommitProtocol")
spark.sql("set spark.sql.legacy.timeParserPolicy=LEGACY")
from delta.tables import *

spark.catalog.clearCache()

# COMMAND ----------

_adhoc_processing_file = datalake_file_location

# COMMAND ----------

df = spark.read.format("csv").option("delimiter", ";").option("header", "true").load(_adhoc_processing_file)


# COMMAND ----------

display(df)

# COMMAND ----------

df = df.withColumn('field_to_joing_in_file_and_Table',F.lit('literal_or_data'))

# COMMAND ----------

#List of fields from file to Update in the table 
COL_FNL = ['field1', 'field2', 'field3', 'field4', 'field5']

_upd_col_lst=','.join("'"+str(x)+"':'file."+str(x)+"'" for x in COL_FNL)
_upd_col='{'+_upd_col_lst+'}'
print("\n Update columne list:")
print(_upd_col)
  
_upd_cond_lst=' OR '.join("NOT(table."+str(x)+"<=>file."+str(x)+")" for x in COL_FNL)
_upd_cond='"'+_upd_cond_lst+'"'
  
print("\n Update condition list:")
print(_upd_cond)

# COMMAND ----------

deltaTable = DeltaTable.forName(spark,'your_staging_schema.your_staging_history_table')

deltaTable2 = DeltaTable.forName(spark,'your_final_schema.your_final_table')

# COMMAND ----------

print("\n Update condition list:")
print(_upd_cond)

# matching_field1 and matching_field2 should EXIST in BOTH table and file

upd_st_hst=f'deltaTable.alias("table").merge(df.alias("file"),"table.matching_field1=file.matching_field1 and table.matching_field2=file.matching_field2").whenMatchedUpdate(condition = {_upd_cond},set ={_upd_col}).execute()'
  
print("\n Update statement for history table:")
print(upd_st_hst)

# COMMAND ----------

# Update history (Staging) table

exec(upd_st_hst)


# COMMAND ----------

spark.sql("refresh table your_staging_schema.your_staging_history_table")

# COMMAND ----------

# matching_field1 and matching_field2 should EXIST in BOTH table and file

upd_st_pdm=f'deltaTable2.alias("table").merge(df.alias("file"),"table.matching_field1=file.matching_field1 and table.matching_field1=file.matching_field1").whenMatchedUpdate(condition = {_upd_cond},set ={_upd_col}).execute()'
  
print("\n Update statement for pdm_ucs_csv table:")
print(upd_st_pdm) 

# COMMAND ----------

# Update Final table

exec(upd_st_pdm)

# COMMAND ----------

spark.sql("refresh table your_final_schema.your_final_table'")
