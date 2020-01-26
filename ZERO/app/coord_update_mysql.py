import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
sys.path.append(r"F:\QHJ\qhj\ZERO")

from concurrent.futures import ThreadPoolExecutor

import pymysql
import numpy as np
import pandas as pd
import requests
from sqlalchemy import create_engine


from tools import *
# geo = Geo()
# regeo = ReGeo()

# regeo(**geo("长沙芙蓉区万象新天8楼815").location).item

def run():
    con = pymysql.connect(**MYSQL_MALL_DIC)
    cursor = con.cursor()



    sql = 'select 订单号,收货地址 from order_details where 国家 is null'
    engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(**MYSQL_MALL_DIC),encoding='utf-8')
    data = pd.read_sql(sql,engine)

    data = completion_col(data,{'国家','省份','城市','县区','街道','lng','lat'})



    start_time('st')


    def submit(index,row,api_name='gaode'):
        geo = Geo(api_name)
        regeo = ReGeo(api_name)
        address= row['收货地址']
        try:
            addrs_component = regeo(**geo(address).location).item
        except ServiceError as e:
            return 
        data.loc[index, '国家'] = addrs_component['国家']
        data.loc[index, '省份'] = addrs_component['省份']
        data.loc[index, '城市'] = addrs_component['城市']
        data.loc[index, '县区'] = addrs_component['县区']
        data.loc[index, '街道'] = addrs_component['街道']

        data.loc[index, 'lat'] = addrs_component['lat']
        data.loc[index, 'lng'] = addrs_component['lng']
        
        
    executor=ThreadPoolExecutor(max_workers=10)

    for index,row in data.iterrows():
    #     submit(index,row)
        executor.submit(submit,index,row)
        
    executor.shutdown(True)    
    print("消耗 %s" %end_time('st'))

    # 处理高德地图 中 地址 为列表的情况
    def d(x,*args,**kargs):
        if x.name in args:
            x = x.apply(lambda y:None if isinstance(y,list) else y)
        return x
    data = data.apply(d,args=('城市','县区','街道'))
    data['县区'][data['县区'].isnull()] = data['城市'][data['县区'].isnull()]

    data[data['国家'].notnull()].to_sql('update_address',engine,index=False,if_exists='replace')


    data[data['国家'].isnull()][['订单号','收货地址']].to_sql('update_address_',engine,index=False,if_exists='replace')

    print('共影响:%s条' %len(data))
    try:
        cursor.callproc('proc_update_address')
        con.commit()
    except:
        pass
    finally:
        con.close()

if __name__ == '__main__':
    run()