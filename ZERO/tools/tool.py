__all__ = ["clear_folder", "get_new_file_path",
             "add_order", 
             "get_tables",
             "start_time", "end_time",
             "Macro"
             ]
import re
import os
import time

import numpy as np
import pandas as pd
from win32com import client 

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

    if "序号" in data.columns:
        del data['序号']

    fields = data.columns.tolist()
    data = data.reset_index(drop=True)
    data.index.name = "序号"
    data = data.reset_index()
    data['序号']  = data['序号'] + 1

    fields.insert(0,'序号')
    return data[fields]


def get_tables(cursor):
    """获取所有表名
    
    通过获取cursor 对象，获取数据库所有的表名
    
    Arguments:
        cursor {conn.curson} -- pymsyql.connnect().cursor()
    
    Returns:
        int,set -- 表数,表名集合
    """
    sql = "show tables"
    tables_count = cursor.execute(sql)
    tables = {table_name[0] for table_name in cursor.fetchall()}
    return tables_count,tables

class DeltaT():
    start_time_dic = {}
    def start_time(self,flag):
        DeltaT.start_time_dic[flag] = time.time()

    def end_time(self,flag):
        
        s_time = DeltaT.start_time_dic.get(flag, None)

        if s_time:
            return time.time() - s_time

        return None

dt = DeltaT()
start_time = dt.start_time
end_time = dt.end_time




# 调用宏文件
class Macro():
    def __init__(self, *macro_params, visible=False, **kargs):
        """
        Arguments:
            *macro_params {[list|tuple]} -- 运行宏的参数
            **kargs {String} -- macro_path : 宏文件路径
                             -- macro_name : 宏名
                             -- oap        : 是否另启进程
        
        Keyword Arguments:
            visible {bool} -- 是否现实Excel文件 (default: {False})
        """

        self.path = kargs.get("macro_path",None)
        self.name = kargs.get("macro_name",None)

        # 当有excel 运行时候 是否开启 新进程
        self.open_anothor_process = kargs.get("oap",True)

        self.params = macro_params

        self.visible = visible

        # 另外开启进程
        if self.open_anothor_process:
            self.xlapp = client.DispatchEx('Excel.Application')
        else:
            self.xlapp = client.Dispatch('Excel.Application')
        self.xlapp.visible = self.visible


    def open(self, path=None):

        self.path = path if path else self.path
        print('>>>>打开宏表')
        self.xlapp.DisplayAlerts = 0
        if path is not None \
            or (path is None \
                and not hasattr(self, 'book') \
                and self.path is not None):
            
            self.book = self.xlapp.Workbooks.Open(self.path)


    def run(self, name=None, params=None, visible=None):
        self.name = name if name else self.name
        if isinstance(params,(list, tuple)):
            self.params = params
        self.visible = self.visible if visible is None else visible

        try:
            self.xlapp.visible = self.visible
            print('>>>>开始运行')
            self.xlapp.Application.Run(self.name, *self.params)
        except Exception as e:
            print(e)


    def close(self):
        print('>>>>关闭宏表')
        self.xlapp.DisplayAlerts = 0
        self.book.Close()
        self.xlapp.Application.Quit()
        print('>>>>关闭完成\n') 


    def __call__(self,**kargs):
        self.run(**kargs)

    def __del__(self):
        try:
            self.xlapp.Application.Quit()
        except:
            pass
