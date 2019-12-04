#!/usr/bin/env python
# coding: utf-8

# In[1]:


from urllib import parse

import os
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from pyquery import PyQuery as pq
import requests

from tools import *


# In[创建连接数据库引擎]
conn_dic = {
    "user":"root",
    "password":"jiuguai",
    "host":"localhost",
    "port":3306,
    "database":"qhj",
    "charset" :"utf8mb4"
}
conn_s = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(**conn_dic)

print('建立数据库连接\n')
engine = create_engine(conn_s, encoding='utf-8')

# In[2]:


start_time('get_goods')
phpsessid = "ik9uh45jlsaih896qopsupoa3s"

mgi = MallGoodsInfo(phpsessid)


# In[3]:

def add_goods(doc):
    goods_l = []
    for tr in doc('tbody tr'):
        d = {}
        d['goods_id'] = tr.xpath('.//img')[0].attrib['goods_id']
        d['goods_name'] = tr.find_class('info_setting')[0].text.strip()
        d['send_price'] = tr.cssselect('input[key=send_price]')[0].attrib['value']
    #   d['send_price'] = tr.xpath('.//input[@key="send_price"]')[0].attrib['value']
    
        d['sort'] = tr.cssselect('input[key=sort]')[0].attrib['value']
    #   d['send_price'] = tr.xpath('.//input[@key="sort"]')[0].attrib['value']
    
        d['shelf'] = tr.cssselect('span[onclick^=opt_shelf]')[0].text
#         d['shelf'] = tr.xpath('.//span[starts-with(@onclick,"opt_shelf")]')[0].text
        
        
        d['tui'] = tr.cssselect('span[onclick^=opt_tui]')[0].text
#         d['tui'] = tr.xpath('.//span[starts-with(@onclick,"opt_tui")]')[0].text
        
        goods_l.append(d)
    return goods_l

# In[4]:


goods_l = []
doc = pq(mgi.get_fgoods())
goods_l.extend(add_goods(doc))


# In[5]:


# 获取其它页信息

item = doc('.pagination>li>a')
max_page = 0
l = []
def t(k,v):

    l.append( v.text)
item.each(t)
if l:
    max_page = int(l[-2])

for page in range(2 ,max_page+1):

    doc = pq(mgi.get_goods(page))
    goods_l.extend(add_goods(doc))


goods_data = pd.DataFrame(goods_l)

print()
# In[6]:


# 商品分类
goods_data['class_name'] = ""
goods_data['class_id'] = ""
for index,row in goods_data.iterrows():

    doc = pq(mgi.get_class(row['goods_id']))
    option = doc("select>option[selected]")[0]
    goods_data.loc[index,"class_id"] = option.attrib['value']
    goods_data.loc[index,"class_name"] = option.text



print()

# In[7]:


# 获取属性信息
attr_l = []


for index,good in goods_data.iterrows():

    attr_l.extend(mgi.get_attrs(good['goods_id'])['select_list'])

attr_data = pd.DataFrame(attr_l)


# In[8]:


def get_attrs(attrs):
    l = []
    for attr in attrs:

        l.append(attr['attr_name'])

    return "|".join(l)

attr_data['attr_name'] = attr_data["attr_name_list"].apply(get_attrs)



# In[9]:


del attr_data['attt_unit']
del attr_data['attr_name_list']
del attr_data['attr_old_price']
goods_info = pd.merge(goods_data, attr_data,on='goods_id',how='left')


# In[16]:

print('存入数据库中')
goods_info.to_sql("sys_goods",engine,if_exists='replace',index=False)



# In[13]:


print("\n", end_time('get_goods'))












