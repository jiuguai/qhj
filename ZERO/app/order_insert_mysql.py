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
for file in os.listdir(sent_dir):
    sent_path = os.path.join(sent_dir,file)
    if not file.startswith("~$") and os.path.isfile(sent_path):
        if file.startswith("趣领_三金"):
            # 处理特殊的三金格式
            sent_data = pd.read_excel(sent_path,converters={"订单号":str},header=3,sheet_name="分销订单")
            sent_data.dropna(subset=['订单号'],inplace=True)
            sent_data = pd.merge(sent_data,goods_map_df,how='left',on='货品编号')
        else:
            sent_data = pd.read_excel(sent_path,converters={"订单号":str})

       
        sent_data['key'] = sent_data['订单号'] + "-" + sent_data['商品ID']
        orders = set(sent_data['key'])

        result = date_com.search(file)
        export_date = result.group()

        src_path = os.path.join(EXPORT_DIR,"订单 %s.xlsx" %export_date)
        src_data = pd.read_excel(src_path,converters={"订单号":str})
        src_data['key'] = src_data['订单号'] + "-" + src_data['商品ID']


        add_data = src_data[src_data['key'].isin(orders)]
        add_data['导出订单时间'] = export_date

        fields = ["订单号", '商品ID', "发货商", "数量", "支付金额", "备注", "收件人", "联系方式", "收货地址", "goods_type",
                  "导出订单时间", '下单时间', '支付时间']
        add_data = add_data[fields]
        add_data = add_data.fillna(value={"备注": "",'支付时间':"1970-01-01 00:00:00"})
        sql = 'insert into order_details(%s) values(%s)' % (','.join(fields), ",".join(np.repeat('%s', len(fields))))
        # sql = 'insert into temp(%s) values(%s)' % (','.join(fields), ",".join(np.repeat('%s', len(fields))))
        for index, row in add_data.iterrows():
            row_data = row.tolist()
            print(row_data)
            cursor.execute(sql, row_data)
            

        conn.commit()
  
        shutil.move(sent_path, os.path.join(ORDER_BK_DIR,file))

conn.close()





