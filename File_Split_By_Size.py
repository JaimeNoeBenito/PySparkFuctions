import datetime
import os
import math

def get_dir_content(ls_path):
    dir_paths = dbutils.fs.ls(ls_path)
    subdir_paths = [get_dir_content(p.path) for p in dir_paths if p.isDir() and p.path != ls_path]
    flat_subdir_paths = [p for subdir in subdir_paths for p in subdir]
    return list(map(lambda p: p.path, dir_paths)) + flat_subdir_paths
    

paths = get_dir_content(path)

for p in paths:
    if(p.find(filename) != -1):
        print("file:" , p)
        c_time = os.path.getctime(p.replace("dbfs:/", "/dbfs/"))
        dt_c = datetime.datetime.fromtimestamp(c_time)
        print('Created on:', dt_c)
        size = os.path.getsize(p.replace("dbfs:/", "/dbfs/"))
        size_print = size
        if(size/1024/1024 > 1):
            size_print = str(round(size/1024/1024,2)) + "MB"
        elif(size/1024 > 1):
            size_print = str(round(size/1024,2)) + "KB"       
        print("size = ", size)
        print("size print = ", size_print)
        
        bloks = math.ceil(size / (int(split_size_KB) * 1024))
        print("bloks =" , bloks)
        
        df = pd.read_csv(p.replace("dbfs:/", "/dbfs/"), delimiter = ";")
        
        file_lines = df.count()[0]
        print("file_lines = ", file_lines)
        
        new_file_lines = math.ceil(file_lines / bloks)
        print("new_file_lines = ", new_file_lines)
        
        file_lines_tmp = file_lines 
        
        df['row_num'] = np.arange(len(df))
        
        init_lines = 0
        n = 1
        while file_lines_tmp+1 >= new_file_lines:
            
            dfn = df[(df['row_num'] > init_lines) & (df['row_num'] <= (init_lines + new_file_lines))]
#             print(dfn.head())
#             print(dfn.tail())

            init_lines = init_lines + new_file_lines
            print("init_lines = ", init_lines)
            
            file_lines_tmp = file_lines_tmp - new_file_lines 
            print("file_lines_tmp = ", file_lines_tmp)
            
            dfn.to_csv(path.replace("dbfs:/", "/dbfs/") + "/" + filename[0:-4] + "_" + str(n) + ".csv", sep=';')
            n = n +1 