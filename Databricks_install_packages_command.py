%sh /databricks/python/bin/pip install --upgrade pip
%sh /databricks/python/bin/pip install pandas==1.3.1
%sh /databricks/python/bin/pip install openpyxl
dbutils.library.restartPython()