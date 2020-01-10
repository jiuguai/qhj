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
    sent_path = os.path.join(sent_dir,file)
    if not file.startswith("~$") and os.path.isfile(sent_path):
        
        sent_data = oxm(file, sent_path)
        if sent_data is None:
            print(">>>>请检查：%s" %file)
            continue

        orders = set(sent_data['key'])
        # print(orders)
        # sys.exit()
        
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

print('更新商品名')
cursor.execute("""
    UPDATE order_details a, goods b
    SET a.goods_name = b.goods_name
    WHERE
        a.goods_name IS NULL
    AND a.商品ID = b.商品ID;
    """)
conn.commit()
conn.close()





