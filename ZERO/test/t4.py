import re
import os
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
sys.path.append(r"E:\dataparse\Python_DATA_PARSE\QHJ\ZERO")
import warnings
warnings.filterwarnings("ignore")
import shutil

import pymysql
import numpy as np
import pandas as pd

from tools import *

qm = QHJMall(MALL_KEY)

"""
将发出去的信息
上传备份
"""

# 连接数据库
conn = pymysql.connect(**MYSQL_MALL_DIC)
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor.execute("select 货品编号, 商品ID from goods where goods_type='free'")
goods_map_dic = cursor.fetchall()
goods_map_df = pd.DataFrame(goods_map_dic)


ORDER_BK_DIR = r"D:\奇货居\work\外发订单\备份\新"


sent_dir = os.path.join(NEW_ORDER_SAVE_DIR,"已发")
date_com = re.compile(r'20\d{2}-\d{1,2}-\d{1,2} \d{1,2}_\d{1,2}_\d{1,2}')
oxm = OrderXlMiddleware(goods_map_df)
for file in os.listdir(sent_dir):
    print(file)
    sent_path = os.path.join(sent_dir,file)
    if not file.startswith("~$") and os.path.isfile(sent_path):
        sent_data = oxm(file, sent_path)
        if sent_data is None: continue
       
        sent_data['key'] = sent_data['订单号'] + "-" + sent_data['商品ID']
        orders = set(sent_data['key'])
        print(orders)

conn.close()





