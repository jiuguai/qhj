#!/usr/bin/env python
# coding: utf-8

# In[1]:


from urllib import parse

import os
import sys
import platform
if platform.node() == "zero_PC":
    sys.path.append(r"F:\QHJ\qhj\ZERO")
else:
    sys.path.append(r"D:\往期\QHJ\ZERO")


import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from pyquery import PyQuery as pq
import requests
import redis
from tools import *


# In[创建连接数据库引擎]
def run():
    
    conn_s = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(**MYSQL_MALL_DIC)

    print('创建数据库连接\n')
    engine = create_engine(conn_s, encoding='utf-8')

    conn = pymysql.connect(**MYSQL_MALL_DIC)
    cursor = conn.cursor()
    # In[2]:








    start_time('get_goods')
    # phpsessid = "ik9uh45jlsaih896qopsupoa3s"

    mg = MallGoods(MALL_KEY)

    mgi = mg


    print('更新 商品类型')

    class_l = mg.get_classes()
    goods_class_data = pd.DataFrame(class_l)
    cursor.execute('delete from goods_class')

    l = []
    for i, row in goods_class_data.iterrows():
        l.append(row.tolist())

        
    sql = "insert into goods_class(class_id,class_name) values(%s,%s)"
    cursor.executemany(sql,l)
    conn.commit()


    # In[3]:
    redis_con = redis.Redis(**REDIS_MALL_ATTR_DIC)

    # 初始化数据库
    redis_con.delete('goods_id')
    redis_con.delete('free_goods_id')
    redis_con.delete('class_id')

    def parse_goods_attr(doc, goods_type='original'):
        goods_l = []
        for tr in doc('tbody>tr'):
            d = {}
            d['goods_id'] = tr.cssselect('.goods_img')[0].attrib['goods_id']

            d['goods_name'] = tr.find_class('info_setting')[0].text.strip()

            d['send_price'] = tr.cssselect('input[key=send_price]')[0].attrib['value']
        #   d['send_price'] = tr.xpath('.//input[@key="send_price"]')[0].attrib['value']
        
            d['sort'] = tr.cssselect('input[key=sort]')[0].attrib['value']
        #   d['send_price'] = tr.xpath('.//input[@key="sort"]')[0].attrib['value']
        
            d['shelf'] = tr.cssselect('span[onclick^=opt_shelf]')[0].text
    #         d['shelf'] = tr.xpath('.//span[starts-with(@onclick,"opt_shelf")]')[0].text

            redis_con.sadd('set_goods_id',d['goods_id'])
            if goods_type=='original':
                d['tui'] = tr.cssselect('span[onclick^=opt_tui]')[0].text
                d['class_name'] = tr.xpath('./td[4]')[0].text
                #         d['tui'] = tr.xpath('.//span[starts-with(@onclick,"opt_tui")]')[0].text
                redis_con.lpush('goods_id',d['goods_id'])
            else:
                redis_con.lpush('free_goods_id', d['goods_id'])



            goods_l.append(d)
        return goods_l

    # In[4]:

    def get_goods(goods_type='original'):
        goods_l = []
        doc = pq(mgi.get_fgoods(goods_type=goods_type))
        goods_l.extend(parse_goods_attr(doc,goods_type=goods_type))
        if goods_type == 'original':
            for option in doc('select[name=class_id]>option')[1:]:
                redis_con.hset('class_id',option.text,option.attrib['value'])

        # In[5]:
        # 获取其它页信息
        item = doc('.pagination>li>a')

        if item.length > 0:
            for page in range(2 ,int(item[-2].text)+1):

                doc = pq(mgi.get_goods(page,goods_type=goods_type))
                goods_l.extend(parse_goods_attr(doc,goods_type=goods_type))

        goods_data = pd.DataFrame(goods_l)

        # In[16]:
        goods_data['goods_type'] = goods_type


        return goods_data

    original_goods_data = get_goods(goods_type='original')
    free_goods_data = get_goods(goods_type='free')
    print('存入数据库中')
    goods_data = pd.concat([original_goods_data,free_goods_data])

    cursor.execute("delete from sys_goods")
    conn.commit()
    goods_data.to_sql("sys_goods",engine,if_exists='append',index=False)


    import goods_sysattr2mysql
#


if __name__ == '__main__':
    run()

