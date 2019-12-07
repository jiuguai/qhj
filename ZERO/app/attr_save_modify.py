import os
import sys
from pprint import pprint
import json
sys.path.append(r"D:\往期\QHJ\ZERO")
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import requests
from tools import *


conn_s = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(**MYSQL_MALL_DIC)
engine = create_engine(conn_s,encoding='utf-8')


# In[]
goods_attr_df = pd.read_sql('select * from sys_goods_details',engine )
goods_attr_df = goods_attr_df[goods_attr_df['attr_name'].notnull()]
#goods_attr_df = goods_attr_df[goods_attr_df['attr_goods_code'].str[0] == 'S']






# In[]

def del_zero_decimal(num):
    try:
        num = num if num % int(num) else int(num)
    except ZeroDivisionError:
        num = 0
    
    return num

def make_attr(index,row):
    attr_name_list = row['attr_name'].split('|')
    
    
    attr_d ={
        
        "attr_list[%s][attr_name]" %(index): row["attr_name"],
        "attr_list[%s][attr_price]" %(index):del_zero_decimal(row["attr_price"]),
        "attr_list[%s][attr_stock]" %(index): int(row["attr_stock"]),
        
        "attr_list[%s][attr_goods_code]" %(index): row["attr_goods_code"],
        "attr_list[%s][goods_id]" %(index): row["goods_id"],
        "attr_list[%s][attr_unit]" %(index): row["attr_unit"],
        "attr_list[%s][attr_old_price]" %(index): del_zero_decimal(row["attr_old_price"]),
     
    }
    
    for attr_name_i,attr_name in enumerate( attr_name_list):
        attr_d ["attr_list[%s][attr_name_list][%s][attr_name]" %(index,attr_name_i)] = \
        attr_name

    return attr_d






# In[标准化上传数据]

attrs_l = []


gdb = goods_attr_df.groupby('goods_id')

for goods_id,df in gdb:


    index = 0
    d = {"goods_id":goods_id}
    for i,row in df.iterrows():

        d.update(make_attr(index,row))
        index += 1

    attrs_l.append(d)





# In[]

with open('test.json','w',encoding='utf-8') as f:
    json.dump(attrs_l,f,ensure_ascii=False)

# In[]
# data = {'attr_list[0][attr_name]': '金色|64G',
#  'attr_list[0][attr_price]': 9300,
#  'attr_list[0][attr_stock]': 100,
#  'attr_list[0][attr_goods_code]': 'S0002P0001C0001P01',
#  'attr_list[0][goods_id]': 7,
#  'attr_list[0][attr_unit]': '部',
#  'attr_list[0][attr_old_price]': 9599,
#  'attr_list[0][attr_name_list][0][attr_name]': '金色',
#  'attr_list[0][attr_name_list][1][attr_name]': '64G',
#  'attr_list[1][attr_name]': '金色|256G',
#  'attr_list[1][attr_price]': 10500,
#  'attr_list[1][attr_stock]': 100,
#  'attr_list[1][attr_goods_code]': 'S0002P0001C0001P02',
#  'attr_list[1][goods_id]': 7,
#  'attr_list[1][attr_unit]': '部',
#  'attr_list[1][attr_old_price]': 10899,
#  'attr_list[1][attr_name_list][0][attr_name]': '金色',
#  'attr_list[1][attr_name_list][1][attr_name]': '256G',
#  'attr_list[2][attr_name]': '金色|512G',
#  'attr_list[2][attr_price]': 12400,
#  'attr_list[2][attr_stock]': 100,
#  'attr_list[2][attr_goods_code]': 'S0002P0001C0001P03',
#  'attr_list[2][goods_id]': 7,
#  'attr_list[2][attr_unit]': '部',
#  'attr_list[2][attr_old_price]': 12699,
#  'attr_list[2][attr_name_list][0][attr_name]': '金色',
#  'attr_list[2][attr_name_list][1][attr_name]': '512G',
#  'attr_list[3][attr_name]': '暗夜绿色',
#  'attr_list[3][attr_price]': 9300,
#  'attr_list[3][attr_stock]': 100,
#  'attr_list[3][attr_goods_code]': 'S0002P0001C0001P04',
#  'attr_list[3][goods_id]': 7,
#  'attr_list[3][attr_unit]': '部',
#  'attr_list[3][attr_old_price]': 9599,
#  'attr_list[3][attr_name_list][0][attr_name]': '暗夜绿色',
#  'attr_list[4][attr_name]': '暗夜绿色',
#  'attr_list[4][attr_price]': 10500,
#  'attr_list[4][attr_stock]': 100,
#  'attr_list[4][attr_goods_code]': 'S0002P0001C0001P05',
#  'attr_list[4][goods_id]': 7,
#  'attr_list[4][attr_unit]': '部',
#  'attr_list[4][attr_old_price]': 10899,
#  'attr_list[4][attr_name_list][0][attr_name]': '暗夜绿色',
#  'attr_list[5][attr_name]': '暗夜绿色',
#  'attr_list[5][attr_price]': 12400,
#  'attr_list[5][attr_stock]': 100,
#  'attr_list[5][attr_goods_code]': 'S0002P0001C0001P06',
#  'attr_list[5][goods_id]': 7,
#  'attr_list[5][attr_unit]': '部',
#  'attr_list[5][attr_old_price]': 12699,
#  'attr_list[5][attr_name_list][0][attr_name]': '暗夜绿色',
#  'attr_list[6][attr_name]': '深空灰色|64G',
#  'attr_list[6][attr_price]': 9200,
#  'attr_list[6][attr_stock]': 101,
#  'attr_list[6][attr_goods_code]': 'S0002P0001C0001P07',
#  'attr_list[6][goods_id]': 7,
#  'attr_list[6][attr_unit]': '部',
#  'attr_list[6][attr_old_price]': 9599,
#  'attr_list[6][attr_name_list][0][attr_name]': '深空灰色',
#  'attr_list[6][attr_name_list][1][attr_name]': '64G',
#  'attr_list[7][attr_name]': '深空灰色|256G',
#  'attr_list[7][attr_price]': 10500,
#  'attr_list[7][attr_stock]': 100,
#  'attr_list[7][attr_goods_code]': 'S0002P0001C0001P08',
#  'attr_list[7][goods_id]': 7,
#  'attr_list[7][attr_unit]': '部',
#  'attr_list[7][attr_old_price]': 10899,
#  'attr_list[7][attr_name_list][0][attr_name]': '深空灰色',
#  'attr_list[7][attr_name_list][1][attr_name]': '256G',
#  'attr_list[8][attr_name]': '深空灰色|512G',
#  'attr_list[8][attr_price]': 12400,
#  'attr_list[8][attr_stock]': 100,
#  'attr_list[8][attr_goods_code]': 'S0002P0001C0001P09',
#  'attr_list[8][goods_id]': 7,
#  'attr_list[8][attr_unit]': '部',
#  'attr_list[8][attr_old_price]': 12699,
#  'attr_list[8][attr_name_list][0][attr_name]': '深空灰色',
#  'attr_list[8][attr_name_list][1][attr_name]': '512G',
#  'attr_list[9][attr_name]': '银色|64G',
#  'attr_list[9][attr_price]': 9200,
#  'attr_list[9][attr_stock]': 100,
#  'attr_list[9][attr_goods_code]': 'S0002P0001C0001P10',
#  'attr_list[9][goods_id]': 7,
#  'attr_list[9][attr_unit]': '部',
#  'attr_list[9][attr_old_price]': 9599,
#  'attr_list[9][attr_name_list][0][attr_name]': '银色',
#  'attr_list[9][attr_name_list][1][attr_name]': '64G',
#  'attr_list[10][attr_name]': '银色|256G',
#  'attr_list[10][attr_price]': 10500,
#  'attr_list[10][attr_stock]': 100,
#  'attr_list[10][attr_goods_code]': 'S0002P0001C0001P11',
#  'attr_list[10][goods_id]': 7,
#  'attr_list[10][attr_unit]': '部',
#  'attr_list[10][attr_old_price]': 10899,
#  'attr_list[10][attr_name_list][0][attr_name]': '银色',
#  'attr_list[10][attr_name_list][1][attr_name]': '256G',
#  'attr_list[11][attr_name]': '银色|512G',
#  'attr_list[11][attr_price]': 12400,
#  'attr_list[11][attr_stock]': 100,
#  'attr_list[11][attr_goods_code]': 'S0002P0001C0001P12',
#  'attr_list[11][goods_id]': 7,
#  'attr_list[11][attr_unit]': '部',
#  'attr_list[11][attr_old_price]': 12699,
#  'attr_list[11][attr_name_list][0][attr_name]': '银色',
#  'attr_list[11][attr_name_list][1][attr_name]': '512G',
#  'goods_id': 7}


# rep = requests.post(url,data=data,headers = headers)
# rep.json()



