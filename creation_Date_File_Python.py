# DBTITLE 1,All files in directory with their creation time
import datetime
import os

def get_dir_content(ls_path):
    dir_paths = dbutils.fs.ls(ls_path)
    subdir_paths = [get_dir_content(p.path) for p in dir_paths if p.isDir() and p.path != ls_path]
    flat_subdir_paths = [p for subdir in subdir_paths for p in subdir]
    return list(map(lambda p: p.path, dir_paths)) + flat_subdir_paths
    

paths = get_dir_content('<your_path')

for p in paths:
    if(p.find("FileNameYouAreLookingFor.Fileextension") != -1):
        print("file:" , p)
        c_time = os.path.getctime(p.replace("dbfs:/", "/dbfs/")) #In case you are working in databricks
        dt_c = datetime.datetime.fromtimestamp(c_time)
        print('Created on:', dt_c)

# COMMAND ----------



# Path to the file
path = r"/dbfs/your_path"

# file modification timestamp of a file
m_time = os.path.getmtime(path)
# convert timestamp into DateTime object
dt_m = datetime.datetime.fromtimestamp(m_time)
print('Modified on:', dt_m)

# file creation timestamp in float
c_time = os.path.getctime(path)
# convert creation timestamp into DateTime object
dt_c = datetime.datetime.fromtimestamp(c_time)
print('Created on:', dt_c)

# COMMAND ----------


