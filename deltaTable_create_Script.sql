CREATE TABLE spark_catalog.your_schema.your_table_name (
  field1 STRING,
  field2 FLOAT,
  field3 TIMESTAMP)
USING delta
LOCATION 'your_dbfs_location'
TBLPROPERTIES (
  'Type' = 'EXTERNAL',
  'delta.minReaderVersion' = '1',
  'delta.minWriterVersion' = '2')