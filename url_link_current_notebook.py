# Databricks notebook source
import json
ctx = json.loads(dbutils.notebook.entry_point.getDbutils().notebook().getContext().toJson())
print(ctx)

# COMMAND ----------

current_path =  ctx['tags']['browserHostName'] + "/?o=" + ctx['tags']['orgId'] + ctx['tags']['browserHash'] 
print(current_path)

# COMMAND ----------


