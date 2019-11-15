import pymysql
from pprint import pprint
conn = pymysql.connect(
        host = "localhost",
        user = "root",
        password = "jiuguai",
        database="qhj",
        charset = "utf8mb4",
    )


cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

sql = """
INSERT INTO test (订单号, 运单号, 商品ID, 商品名, 下单用户, 售价,下单时间, 收件人电话, 收件人地址, 供应商) VALUES ('2019102319289237690x', null, 'S0005C0001P02', 'iPhone 11 Pro MAX 深空灰色|512GB|4G全网通 市场价12699元', 'sx',123.416, '2019-11-10 12:30:21', '13910300718', '北京市昌平区北七家镇温泉花园B区70-361', 'S0005C0001P02');


"""
cursor.execute(sql)
cursor.executemany( )

conn.commit()
cursor.close()
conn.close()




"""
# 查询数据
sql = "select left(供应商,5) as 供应商ID from test;"



cursor.execute(sql)
# ret = cursor.fetchall()
ret = cursor.fetchone()
ret1 = cursor.fetchmany(2)

pprint(ret)
print('-'*20)
pprint(ret1)

调用

"""