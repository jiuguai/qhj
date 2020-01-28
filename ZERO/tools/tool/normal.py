__all__ = ["clear_folder", "get_new_file_path",
             "add_order", 
             "get_tables",
             "completion_col","get_duplicated_field",
             "start_time", "end_time",
             "Macro","MyEncoder",
             "read_xl",
             "PDFTool"
             ]
import re
import os
import json
import time

import datetime

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


# 补齐需要的缺省列
def completion_col(data, fields, format_dict={}):
    """补齐dataframe缺省列
    
    补齐列
    
    Arguments:
        data {dataframe} -- 需要补齐的dataframe
        fields {set()} -- 需要补齐的自断
    
    Keyword Arguments:
        format_dict {dict} -- fields中默认值 如果为空默认补齐为None (default: {{}})
    
    Returns:
        [dataframe] -- [返回已补齐的dataframe]
    """
    data_fields = set(data)
    for field in (fields - data_fields):
        default_value = format_dict.get(field, None)
        data[field] = default_value
    return data

def get_duplicated_field(df_columns):
    """get_duplacetes
    
    将集合中重复的返回重复想
    
    Arguments:
        columns {[list,tuple]} -- 集合类型数据
    
    Returns:
        set -- 重复数据
    """
    
    assert isinstance(df_columns,(list,tuple)),"预期 (list,tuple) 实际传入 %s" %(type(df_columns))
    duplicated_fileds = set({})
    columns = set({})
    for filed_name in df_columns:
        if filed_name not in columns:
            columns.add(filed_name)
        else:
            duplicated_fileds.add(filed_name)
    return duplicated_fileds


# 获取数据库表名
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


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        else:
            return super(MyEncoder, self).default(obj)


# 寻找最合适 有匹配字段的 sheet
def read_xl(file_name, *args, deep_search_row=5, index=False,**kargs):

    if len(args) > 0:
        compare_fields = args[0]
    else:
        compare_fields = False

    if not compare_fields:
        data = pd.read_excel(file_name,index=index,
            sheet_name=kargs.get('sheet_name',0),
            header=kargs.get('header',0))    
        return data

    file_obj = pd.ExcelFile(file_name)
    if isinstance(compare_fields,(list,tuple)):
        compare_fields = set(compare_fields)
    elif isinstance(compare_fields,str):
        compare_fields = {compare_fields}
    

    if 'sheet_name' in kargs:
        sheet_names = [kargs.get("sheet_name")]
    else:
        sheet_names = file_obj.sheet_names


    for sht_name in sheet_names:
        sht = file_obj.book.sheet_by_name(sht_name)
        
        search_row = deep_search_row if sht.nrows >= deep_search_row else sht.nrows
        # print(sht.nrows,search_row)
        
        for row in range(search_row):
            if compare_fields <= set(sht.row_values(row)):
                data = file_obj.parse(sheet_name=sht_name,header=row,index=index,**kargs)
                return data




# PDF 工具
class PDFTool():

    @staticmethod
    def pdf_split(file_path, result_dir, suffix=""):
        from PyPDF2 import PdfFileReader, PdfFileWriter
        with open(file_path, 'rb') as f:
            reader = PdfFileReader(f)

            nums = reader.getNumPages()
            for page in range(nums):
                writer = PdfFileWriter() 
                writer.addPage(reader.getPage(page))
                out_file = os.path.join(result_dir, "%s%s.pdf" %(str(page+1).zfill(3), suffix))

                print('拆分 第%s页 ' %(page+1))
                with open(out_file, 'wb') as outf:
                    writer.write(outf)


    @staticmethod
    def pdf_merge(file_dir, out_file_path):
        from PyPDF2 import PdfFileReader, PdfFileWriter
        writer = PdfFileWriter() 
        files = [os.path.join(file_dir, file_name) for file_name in os.listdir(file_dir) 
                    if file_name.endswith('pdf')
        ]
        file_objs = [open(file_path, 'rb') for file_path in files
                    if os.path.isfile(file_path)]

        # print(file_objs)

        for obj in file_objs:
            reader = PdfFileReader(obj)
            nums = reader.getNumPages()
            print(obj)
            for page in range(nums):
                print(page)
                writer.addPage(reader.getPage(page))

        with open(out_file_path, 'wb') as outf:
            writer.write(outf)

        for obj in file_objs:
            obj.close()


    @staticmethod
    def extract_table(pdf_path, pages='all', mode="L"):
        """
        Arguments:
            pdf_path {str} -- path
        
        Keyword Arguments:
            pages {str} --  (default: {'all'})
                  {list} -- [1, 2, 3]
            mode {str} -- L return List
                       -- D return DataFrame List

        """
        mode = mode.upper()
        if mode == "L":
            import pdfplumber

            with pdfplumber.open(pdf_path) as pdf:
                pdf_pages = pdf.pages
                page_count = len(pdf_pages)

                print("共%s 页" %page_count)
                if pages == "all":
                    pages = range(page_count)
                else:
                    pages = [page-1 for page in pages]

                data = []

                for page in pages:
                    for row in pdf_pages[page].extract_tables():
                        data.extend(row)

                return data

        elif mode == "D":
            import tabula
            tables = tabula.read_pdf(pdf_path, pages=pages) 
            print("共%s 页" %len(tables))

            return tables