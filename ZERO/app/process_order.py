#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")

import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine


import warnings

warnings.filterwarnings('ignore')
from tools import *

start_time('handle_order')


# 初始化数据库连接，使用pymysql模块
conn_dic = {
    "user":"root",
    "password":"jiuguai",
    "host":"localhost",
    "port":3306,
    "database":"qhj",
    "charset" :"utf8mb4"
}
conn_s = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(**conn_dic)

engine = create_engine(conn_s, encoding='utf-8')
print('连接数据库')
conn = pymysql.connect(**conn_dic)
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor = conn.cursor()
tables_count, tables = get_tables(cursor)

lt_time = None
fm_lt_time = None


# In[2]:


"""
读取数据

"""


# In[3]:




# 读取 供应商信息
print('读取供应商信息')
commodity_df = pd.read_excel(COMMODITY_PATH)


commodity_df = commodity_df[['商品ID','供应商ID','供应商',"发货商","发货商ID"]]

# 读取导出信息

order_path, lt_time = get_new_file_path(EXPORT_DIR,ORDER_DATE_PATT)
fm_lt_time = lt_time.strftime(DATE_FORMAT)

print('读取 %s' %order_path)
data = pd.read_excel(order_path)
data = OrderInMiddleware(data)()

data['导出订单时间'] = lt_time

print('>>>>系统字段统一为本地字段')
data.rename(columns=FIELDS_SLM_DIC,inplace=True)


# 获取供应商
print('>>>>连接供应商信息')
data = pd.merge(data,commodity_df,how='left',on='商品ID')



# In[4]:


"""
分离更新 还是 插入的数据
"""


# In[5]:


# 处理系统导出的数据表

print('>>>>将订单分离为 需要更新 和 需要外发两部分\n')
up_order_df = None
if "运单号" in data.columns:
    # 需要更新的信息
    up_order_df = data[data['运单号'].notnull()]
    # 产生的新订单
    new_order_df = data[data['运单号'].isnull()]
else:
    new_order_df = data.copy()


# In[6]:


"""
存储 及备 份
"""


# In[7]:


# 存储新订单信息

if len(new_order_df):
    print("存储订外发单信息")
    new_order_path = os.path.join(NEW_ORDER_BAK_DIR,"订单 %s.xlsx" %(fm_lt_time))
    print('>>>>备份')
    new_order_df.to_excel(new_order_path)
    print('>>>>存入临时数据库 export_order')
    new_order_df.to_sql("export_order",engine,if_exists='replace',index=False)

    
# 存储需更新信息
if up_order_df is not None and len(up_order_df):
    print('备份更新信息')
    up_order_path = os.path.join(UPDATE_ORDER_BAK_DIR,"订单 %s.xlsx" %(fm_lt_time))
    print('>>>>备份')
    up_order_df.to_excel(up_order_path)
    print('>>>>存入临时数据库 up_order')
    up_order_df.to_sql("up_order",engine,if_exists='replace',index=False)



print()


# In[8]:


# 调用存储过程

# 调用 将订单分为 新和超时订单 的存储过程
print('调用处理订单的存储过程')

print('>>>>调用存储过程 proc_export_order')
cursor.callproc("proc_export_order",(OVERTIME_ORDER_TO_WAYBILL_HOUR,))
conn.commit()
print('>>>>完成提交')

print('>>>>调用存储过程 proc_insert_new_order')
cursor.callproc("proc_insert_new_order")
conn.commit()
print('>>>>完成提交')



print()


# In[9]:


# 生成外发的订单

print('读取新订单信息 temp_new_order')
sql = "select * from temp_new_order"
new_order_df = pd.read_sql(sql, engine)

print('读取已发订单 未超时 temp_old_order')
sql = "select * from temp_old_order"
old_order_df = pd.read_sql(sql, engine)


print('两表初步处理')
fields =  ["订单号",'运单号',"商品ID",'供应商','商品名','数量','规格','单位','收件人姓名','收件人地址','收件人电话','备注','发货商']

new_order_df['运单号'] = ""
old_order_df['运单号'] = ""

if '备注' not in new_order_df:
    new_order_df['备注'] = ""
    old_order_df['备注'] = ""

new_order_df_r = new_order_df[fields]
old_order_df_r = old_order_df[fields]

print()


# In[10]:


print('存储新订单 %s' %NEW_ORDER_SAVE_DIR)
odo = OrderOutMiddleware(new_order_df_r,"发货商")
for d_plat in new_order_df_r['发货商'].unique():
    temp = odo.out(d_plat)
    file_name = "%s_新订单 %s.xlsx" %(d_plat,fm_lt_time)
    file_path = os.path.join(NEW_ORDER_SAVE_DIR,file_name)
    
    print('>>>>正在存储 %s' %(file_name))
    temp.to_excel(file_path,index=False,sheet_name="新订单")    
print("新订单存储完成\n")

print('存储已发未回订单 %s' %OVERTIME_ORDER_SAVE_DIR)
odo = OrderOutMiddleware(old_order_df_r,"发货商")
for d_plat in old_order_df_r['发货商'].unique():
    temp = odo.out(d_plat)
    file_name = "%s_已发未回订单 %s.xlsx" %(d_plat,fm_lt_time)
    file_path = os.path.join(OVERTIME_ORDER_SAVE_DIR,file_name)
    
    print('>>>>正在存储 %s' %(file_name))
    temp.to_excel(file_path,index=False,sheet_name="已发未回")    

print("已发未回订单存储完成\n")


# In[11]:


macro_path = BEAUTY_VBA_PATH
macro_name = "美化.xlsm!beautify"
macro_params = r"D:\奇货居\work\外发订单\新订单\|D:\奇货居\work\外发订单\已发未收\\"


mo = Macro(visible=EXCEL_VISIBLE)
mo.open(macro_path)
mo(name=macro_name,params = (macro_params,))
mo.close()

print("%0.3fs\n" %end_time('handle_order'))

