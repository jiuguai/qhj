
import re
import os
import numpy as np
import pandas as pd

def clear_folder(target_dir,is_recursion=True):
    for file in os.listdir(target_dir):
        path = os.path.join(target_dir,file)
        if os.path.isfile(path):
            os.remove(path)
        elif is_recursion and os.path.isdir(path):
            try:
                os.rmdir(path)
            except OSError:
                clear_folder(path)
                os.rmdir(path)


def get_new_file_path(file_dir,file_date_patt,date_format="%Y-%m-%d %H_%M_%S",recursion=False):
    
    order_com = re.compile(file_date_patt)

    date = pd.to_datetime("1900-1-1")
    max_date_file_path = ""
    
    # 
    if recursion:
        # 递归遍历
        _file_dir = file_dir
        for file_dir,dir_name,file_names in os.walk(_file_dir):

            for file_name in file_names:
                order_date = order_com.match(file_name)
                if order_date:
                    order_date = order_date.groupdict()['date']

                    order_date = pd.to_datetime(order_date,format= date_format)
                    if order_date > date:
                        date = order_date
                        max_date_file_path = os.path.join(file_dir,file_name)
    else:
        # 遍历当前目录
        for file_name in os.listdir(file_dir):

            order_date = order_com.match(file_name)

            if order_date:
                order_date = order_date.groupdict()['date']

                order_date = pd.to_datetime(order_date,format= date_format)
                if order_date > date:
                    date = order_date
                    max_date_file_path = os.path.join(file_dir,file_name)

    

    return max_date_file_path,date


def add_order(data):
    fields = data.columns.tolist()
    if "序号" in fields:
        del data['序号']
    data = data.reset_index(drop=True)
    data.index.name = "序号"
    data = data.reset_index()
    data['序号']  = data['序号'] + 1

    fields.insert(0,'序号')
    return data[fields]


def get_tables(cursor):
    sql = "show tables"
    tables_count = cursor.execute(sql)
    tables = {table_name[0] for table_name in cursor.fetchall()}
    return tables_count,tables