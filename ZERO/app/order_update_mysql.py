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



conn = pymysql.connect(**MYSQL_MALL_DIC)
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
ORDER_BK_DIR = r"D:\奇货居\work\外发订单\备份\反馈"

recv_dir = os.path.join(NEW_ORDER_SAVE_DIR,"反馈数据")

cursor.execute("select 货品编号, 商品ID from goods where goods_type='free'")
goods_map_dic = cursor.fetchall()
goods_map_df = pd.DataFrame(goods_map_dic)

sql = "update order_details set 运单号=%s, 快递公司=%s where 订单号=%s and 商品ID=%s"

fiels = ['运单号','快递公司','订单号','商品ID']
re_col = {
    "快递方式":"快递公司"
    
}
for file in os.listdir(recv_dir):
    recv_file_path = os.path.join(recv_dir,file)
    if not file.startswith('~$') and os.path.isfile(recv_file_path):
        data = pd.read_excel(recv_file_path,converters={"订单号":str,"运单号":str})
        if "运单号" not in data.columns:
            data = pd.read_excel(recv_file_path,converters={"订单号":str,"运单号":str},sheet_name="分销订单", header=3)
            
            data = pd.merge(data,goods_map_df,how='left',on='货品编号')


        data.dropna(subset=['运单号'],inplace=True)
        data.rename(columns=re_col,inplace=True)
        data = data[fiels]

        for index, row in data.iterrows():
            row_data = row.tolist()
            print(row_data)
            cursor.execute(sql,row_data)
        conn.commit()
        shutil.move(recv_file_path,os.path.join(ORDER_BK_DIR,file))
conn.close()

