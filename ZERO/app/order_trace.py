import sys
import platform
if platform.node() == "zero_PC":
    sys.path.append(r"F:\QHJ\qhj\ZERO")
else:
    sys.path.append(r"D:\往期\QHJ\ZERO")
import os
import json

import numpy as np
import pandas as pd

import redis
from sqlalchemy import create_engine
from coord_convert.transform import gcj2bd



import pymysql

from tools import *
def run():

    start_time('order_trace')
    conn = pymysql.Connect(**MYSQL_MALL_DIC)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    engine_conn = "mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(**MYSQL_MALL_DIC)
    engine = create_engine(engine_conn,encoding='utf-8')
    save_dir = r"D:\往期\QHJ\echart"


    # order_df = pd.read_sql('select * from order_details where 下单时间>="2019-12-01 00:00:00"',engine)
    goods_df = pd.read_sql('select * from goods',engine,)
    cursor.execute('select * from order_details where 下单时间>="2019-12-01 00:00:00"')
    d = cursor.fetchall()
    order_df = pd.DataFrame(d)


    free_order = order_df[order_df['goods_type']=="free"]

    sg_free_order = free_order[free_order['goods_name'].str[:2] == "三金"]
    df = pd.merge(sg_free_order,goods_df[["商品ID","SPUID",'系统分类','市场价','成本价','售价','发货商','发货商ID','规格','单位']],on='商品ID',how='left')
    df['lat'] = df['lat'].astype(np.float64)
    df['lng'] = df['lng'].astype(np.float64)

    df.reset_index(drop=True,inplace=True)
    # 转换为 百度坐标系
    def convert_coord(coord):
        coord_r = gcj2bd(*coord.tolist())

        coord['lng'] = coord_r[0]
        coord['lat'] = coord_r[1]
        return coord
    df_coord = df[['lng','lat']].apply(convert_coord,axis=1)
    del df['lng']
    del df['lat']
    df = pd.concat([df,df_coord],axis=1)

    pd.set_option('mode.chained_assignment',None)
    # 运单未回部分
    df_r = df[['goods_name','下单时间','订单号','导出订单时间','运单号']]
    df_r = df_r.replace({"goods_name":{r".+?\((.+?)\)$":r"\1"}},regex=True)
    df_r['发货状态'] = "已回复"

    df_r['发货状态'][df_r['运单号'].isnull()] = "待回复"
    del df_r['运单号']

    df_r['对接日期'] = df_r['导出订单时间'].apply(lambda x:x.strftime('%Y-%m-%d'))
    df_r['下单日期'] = df_r['下单时间'].apply(lambda x:x.strftime('%Y-%m-%d'))
    df_r.sort_values('导出订单时间',inplace=True)
    df_r.reset_index(drop=True,inplace=True)

    # 当天订单 当天对接
    df_r['current_day'] = "非当日"
    df_r['current_day'][df_r['对接日期'] == df_r['下单日期']] = "当日"
    data_d = {}

    data = {
        "xaxis":[],
        "order_data":[], # 下单数
        "abut_data":[], # 对接数 分为回复 和 待回复
    #     "not_abut_data":[],
        "goods_order":[], # 按商品 分类 订单总数
        "cur_vs_abut_order":[],# 当天 和 非当前 唯独
        "abut_details":{}, # 下单详情
        "order_details":{}
    }

    temp = df_r[['对接日期','goods_name','订单号','发货状态','current_day']]
    # temp['发货状态'] = np.random.choice(['已回复','待回复'],len(temp))

    agg = temp.groupby(["对接日期",'goods_name'])
    l = []

    for (date,goods_name),row in agg:
    #     print(date,goods_name)
        d = {
            '对接日期':date,
            "goods_name":goods_name,
            '对接数':row['订单号'].count(),
            
        }
        
        d.update(row['发货状态'].value_counts().to_dict())
        
        d.update(row['current_day'].value_counts().to_dict())
        data['abut_details'].setdefault(date,{})

        data['abut_details'][date].update({goods_name:d})
        
        
        l.append(d)
    # print(l)
    abut_temp = pd.DataFrame(l)
    abut_temp = abut_temp.fillna(0)
    abut_temp = abut_temp.groupby("对接日期").sum().sort_index()


    # 获取下单总数
    goods_name_d = temp[['订单号','goods_name']].rename(columns={"订单号":"下单数"}).groupby('goods_name').count().to_dict()['下单数']
    data['goods_order'] = [{"name":key,"value":v} for key,v in goods_name_d.items()]

    # 获取下单信息
    order_temp = df_r[['下单日期','goods_name','订单号']]
    order_agg = order_temp.groupby(['下单日期','goods_name'])

    for (date,goods_name),row in order_agg:
        d = {
            "下单日期":date,
            "goods_name":goods_name,
            "下单数":row['订单号'].count()
        }
        data['order_details'].setdefault(date,{})
        data['order_details'][date].update({goods_name:d})
        
        
    order_temp = df_r[['下单日期','订单号']].rename(columns={"订单号":"下单数"}).groupby('下单日期').count()



    main_temp = pd.concat([abut_temp,order_temp],axis=1,sort=False).sort_index().fillna(0)
    data['xaxis'] = main_temp.index.tolist()

    data['order_data'] = {"name":"下单数",
                          "data":main_temp['下单数'].tolist(),
                          
                        }

    data['abut_data'] = []
    for col in {'已回复','待回复'} & set(main_temp):
        data['abut_data'].append({'name':col,'data':main_temp[col].tolist()})

    data['cur_date'] = main_temp['当日'].to_dict()
    data['ncur_date'] = main_temp['非当日'].to_dict()


    # js_path = os.path.join(save_dir,r'data\new_order.json')
    # with open(js_path,"w",encoding='utf-8') as f:

    #     f.write('order_data=')

    #     json.dump(data,f,ensure_ascii=False,cls=MyEncoder)    
        
        


    REDIS_MALL_ORDER_DIC_ALI = {'host': '47.105.186.249', 'port': 6379, 'db': 0,"password":"r-jiuguai", 'decode_responses': True}

    rd = redis.Redis(**REDIS_MALL_ORDER_DIC_ALI)
    result = rd.set("qhj:summary",json.dumps(data,ensure_ascii=False,cls=MyEncoder))

    print(result)
    end_time('order_trace')


if __name__ == '__main__':
    run()
