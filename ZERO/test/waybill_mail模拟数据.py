import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine

con_dic = {
	"user":"root",
	"password": "jiuguai",
	"host":"localhost",
	"port":3306,
	"database":"qhj",
	"charset":"utf8mb4"
}
conn = pymysql.connect(**con_dic)

cur = conn.cursor()


cur.execute("delete from waybill_mail")
conn.commit()
engine = create_engine("mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(**con_dic),encoding='utf-8')

data_path = r"C:\Users\qhj01\Desktop\MysSql_orderdetails_data.xlsx"
fields = ["订单号", "运单号", "商品名", "规格", "单位", "数量", "收件人姓名", "收件人地址", "收件人电话", "备注"]
data = pd.read_excel(data_path)
data['备注'] = ""
data = data[1:5][fields]

data.to_sql("waybill_mail",engine,if_exists="append",index=False)

