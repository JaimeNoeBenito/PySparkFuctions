%sh /databricks/python/bin/pip install --upgrade pip
%sh /databricks/python/bin/pip install pandas==1.3.1
%sh /databricks/python/bin/pip install openpyxl
dbutils.library.restartPython()
xl = pd.ExcelFile(directory, engine='openpyxl')
excel_sheets = xl.sheet_names
df = xl.parse()
df