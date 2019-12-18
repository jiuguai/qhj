#!/usr/bin/env python
# coding: utf-8

# In[1]:

from concurrent.futures import ThreadPoolExecutor
from threading import Thread,Lock,active_count,enumerate
import time

import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
import warnings
warnings.filterwarnings('ignore')
import redis

import pymysql

from pyquery import PyQuery as pq


from tools import *

lock = Lock()
# In[创建连接数据库引擎]
conn = pymysql.connect(**MYSQL_MALL_DIC)
# cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
cursor = conn.cursor()
cursor.execute('delete from sys_goods_attr')
conn.commit()
# 连接redis
redis_con = redis.Redis(**REDIS_MALL_ATTR_DIC)

redis_con.delete('set_goods_id')

commit_total = 0

# phpsessid = "ik9uh45jlsaih896qopsupoa3s"
# 访问商城的数据
mgi = MallGoodsInfo(MALL_KEY)

# 建立redis连接
redis_con = redis.Redis(**REDIS_MALL_ATTR_DIC)

add_class_sql = r"update sys_goods set class_name=%s where goods_id = %s"

add_attr_sql  = r"""insert into sys_goods_attr(goods_id, attr_goods_code, attr_name, attr_price, attr_stock, attr_unit, attr_old_price) values(
%s, %s, %s, %s, %s, %s, %s
)
"""


def commit_class(goods_id, goods_type='original'):
    global commit_total
    doc = pq(mgi.get_class(goods_id, goods_type=goods_type))
    class_name = doc("select>option[selected]")[0].text
    try:
        lock.acquire()
        cursor.execute(add_class_sql, ( class_name, goods_id))
        conn.commit()
        commit_total += 1
        lock.release()
    except Virtual:
        pass
    finally:
        try:
            lock.release()
        except:
            pass

def commit_attr(goods_id, goods_type='original'):
    global commit_total
    select_list = mgi.get_attrs(goods_id, goods_type=goods_type)['select_list']
    for attr in select_list:
        attr_list = attr['attr_name_list']
        attr_name = "|".join([attr['attr_name'] for attr in attr_list ])
        attr_price = attr['attr_price']
        attr_stock = attr['attr_stock']
        attr_goods_code = attr['attr_goods_code']
        attr_old_price = attr['attr_old_price']
        attr_unit =  attr['attr_unit']

        try:
            lock.acquire()
            cursor.execute(add_attr_sql, args=(goods_id, attr_goods_code, attr_name, attr_price, attr_stock, attr_unit, attr_old_price))
            conn.commit()
            commit_total += 1
            lock.release()
        except Virtual:
            pass
        finally:
            try:
                lock.release()
            except:
                pass

def add_free_goods_attr():

    while True:
        try:
            free_goods_id_tuple = redis_con.brpop('free_goods_id',  0)
        except SystemExit:
            conn.close()
        if free_goods_id_tuple is not None:
            free_goods_id = free_goods_id_tuple[1]
            # commit_class(free_goods_id,goods_type='original') # 还未有此需求
            commit_class(free_goods_id,goods_type='free')
            redis_con.sadd('set_goods_id', free_goods_id)

def add_goods_attr():

    while True:
        try:
            goods_id_tuple = redis_con.brpop('goods_id', 0)
        except SystemExit:
            conn.close()

        print(goods_id_tuple)
        if goods_id_tuple is not None:
            goods_id = goods_id_tuple[1]
            commit_attr(goods_id, goods_type='original')
            # commit_attr(goods_id,goods_type='free') # 还未有此需求
            redis_con.sadd('set_goods_id', goods_id)

def manager(wake_time=5):
    global commit_total
    status = commit_total
    limit_count = 2
    eq_count = 0
    while True:
        time.sleep(wake_time)
        print('%s %s' %(status, commit_total))
        if status == commit_total and eq_count >= limit_count:
            print('调用存储过程 goods_info + attr_inof -> details ,update old_price')
            cursor.callproc('pro_goods_details')
            conn.commit()
            conn.close()
            print('爬取 结束')
            sys.exit()



        elif status == commit_total and eq_count < limit_count:
            eq_count += 1
        else:
            status = commit_total
            eq_count = 0

t_l = []
t_l.append(Thread(target=add_goods_attr))
t_l.append(Thread(target=add_goods_attr))
t_l.append(Thread(target=add_goods_attr))
t_l.append(Thread(target=add_goods_attr))
t_l.append(Thread(target=add_free_goods_attr))
for t in t_l:
    t.setDaemon(True)
    t.start()
Thread(target=manager,kwargs={"wake_time":2}).start()
for t in t_l:t.join()



# excutor = ThreadPoolExecutor(max_workers=5)
# futures = []
# futures.append(excutor.submit(add_goods_attr))
# futures.append(excutor.submit(add_goods_attr))
# futures.append(excutor.submit(add_goods_attr))
# futures.append(excutor.submit(add_free_goods_attr))
# futures.append(excutor.submit(add_goods_attr))
#
# excutor.shutdown(True)





#
#





















