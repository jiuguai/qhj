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

data['订单号'] = data['订单号'].astype(str)
data['联系方式'] = data['联系方式'].astype(str)
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

# 存储新订单信息

fields =  ["订单号","商品ID",'供应商','商品名','数量','规格','单位','收件人','收货地址','联系方式','备注','发货商']
new_order_df = data.copy()
if len(new_order_df):
    print("存储订外发单信息")
    new_order_path = os.path.join(NEW_ORDER_BAK_DIR,"订单 %s.xlsx" %(fm_lt_time))
    print('>>>>备份')
    new_order_df.to_excel(new_order_path)



new_order_df_r = new_order_df[fields]

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




# In[11]:


macro_path = BEAUTY_VBA_PATH
macro_name = "美化.xlsm!beautify"
macro_params = (r"D:\奇货居\work\外发订单\新订单\|D:\奇货居\work\外发订单\已发未收\\",
    r"(?:新订单|已发未回订单)(?= 20\d{2}(?:-\d{1,2}){2}\D+?\d{1,2}(?:_\d{1,2}){1,2}\.xlsx$)",
    r"新订单|已发未回",
    "外发订单"
    )


mo = Macro(visible=EXCEL_VISIBLE)
mo.open(macro_path)
mo(name=macro_name,params = macro_params)
mo.close()

print("%0.3fs\n" %end_time('handle_order'))

