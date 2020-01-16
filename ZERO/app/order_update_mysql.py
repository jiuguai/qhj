import re
import os
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
sys.path.append(r"F:\QHJ\qhj\ZERO")
import warnings
warnings.filterwarnings("ignore")
import shutil

import pymysql
import numpy as np
import pandas as pd

from tools import *

qm = QHJMall(MALL_KEY)



conn = pymysql.connect(**MYSQL_MALL_DIC)
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
ORDER_BK_DIR = r"D:\奇货居\work\外发订单\备份\反馈"

recv_dir = os.path.join(NEW_ORDER_SAVE_DIR,"反馈数据")

cursor.execute("select 货品编号, 商品ID from goods where goods_type='free'")
goods_map_dic = cursor.fetchall()
goods_map_df = pd.DataFrame(goods_map_dic)
wxm = WaybillXlMiddleware(goods_map_df)

sql = "update order_details set 运单号=%s, 快递公司=%s where 订单号=%s and 商品ID=%s"


for file in os.listdir(recv_dir):
    recv_file_path = os.path.join(recv_dir,file)
    if not file.startswith('~$') and os.path.isfile(recv_file_path):
        print(file)
        data = wxm(file, recv_file_path)

        data.dropna(subset=['运单号'], inplace=True)
        for index, row in data.iterrows():
            row_data = row.tolist()
            print(row_data)
            cursor.execute(sql,row_data)
        conn.commit()
        shutil.move(recv_file_path,os.path.join(ORDER_BK_DIR,file))
conn.close()

