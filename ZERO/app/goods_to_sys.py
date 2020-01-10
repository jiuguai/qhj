import re
import os
from random import randint
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
sys.path.append(r"E:\dataparse\Python_DATA_PARSE\QHJ\ZERO")
from pyquery import PyQuery as pq
import requests
from sqlalchemy import create_engine
import pymysql
import pandas as pd

from tools import *


conn = pymysql.Connect(**MYSQL_MALL_DIC)
cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute('select * from goods_class')
goods_class = pd.DataFrame(cursor.fetchall())
goods_class_dic = dict(zip(goods_class['class_name'],goods_class['class_id']))
mg = MallGoods(MALL_KEY)

spu_data = read_xl(COMMODITY_PATH,sheet_name="未上传")
# test
# spu_data = read_xl(COMMODITY_PATH,sheet_name="SPU")[:2]

spu_data['class_id'] = spu_data['系统分类'].apply(lambda x:goods_class_dic[x])
spu_data['goods_name'] = spu_data['商品名简称']

df = spu_data[['goods_name','goods_id','goods_type','class_id']]
mg.add_goods(df)