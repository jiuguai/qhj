#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import sys
import platform
if platform.node() == "zero_PC":
    sys.path.append(r"F:\QHJ\qhj\ZERO")
else:
    sys.path.append(r"D:\往期\QHJ\ZERO")



import warnings
warnings.filterwarnings("ignore")

from pyquery import PyQuery as pq
import requests
from urllib.parse import urlencode,parse_qs
import numpy as np
import pandas as pd
import redis

import pymysql

import json
from tools import *

import datetime

MAX_DELAY_DAY = 100

def run():
    qm = QHJMall(MALL_KEY)
    lt_time = None
    fm_lt_time = None


    # In[2]:
    def dup_order(key):
        if r_conn.sismember('order:old',key):
            return None
        return key

    """
    读取数据

    """
    # 读取 供应商信息

    start_time('handle_order')


    print('读取供应商信息')
    commodity_df = pd.read_excel(COMMODITY_PATH)

    
    # In[3]:

    sku_goods = commodity_df \
                    [['商品ID', '发货商','发货商ID',"货品编号",'goods_type','规格','单位', '市场价','售价','商品名简称', '发货货品名']] \
                    .rename(columns={"售价":"单价","商品名简称":"商品名"}).fillna({"goods_type":"original"})
    
    sku_goods['商品名'][(sku_goods['发货货品名'].notnull())] = \
    sku_goods['发货货品名'][(sku_goods['发货货品名'].notnull())]



    commodity_df = commodity_df[['商品ID','供应商ID','供应商',"发货商","发货商ID"]]
    # 清理环境
    clear_folder(NEW_ORDER_SAVE_DIR, is_recursion=False)


    # 更新 去重环境

    r_conn = redis.Redis(**REDIS_MALL_ORDER_DIC)
    conn = pymysql.connect(**MYSQL_MALL_DIC)
    cursor = conn.cursor()

    

    result = cursor.execute("select CONCAT(订单号,'-',商品ID) as k from order_details where 下单时间>='%s';" 
                            %(datetime.date.today() - datetime.timedelta(MAX_DELAY_DAY)).strftime("%Y-%m-%d"))


    
    r_conn.delete('order:old')
    if result > 0:
        r_conn.sadd('order:old',*[ key[0] for key in cursor.fetchall()])


    # 免费商品名映射SPUID
    cursor.execute("select goods_sys_name, SPUID from fg_map_spuid")
    free_goods_map = pd.DataFrame(list(cursor.fetchall()), columns=['商品名', '商品ID'])


    ## 获取免费的最新订单
    #同步

    # l = []
    # for order in qm.gen_orders("free",order_status=1):
    #     l.append(order)
        
    # data = pd.DataFrame(l)

    # 异步
    start_time('free_get_orders')
    data = qm.async_get_orders('free', 1, coroutine_max=100)
    print('-->free 耗时:%s' %(end_time('free_get_orders')))

    if len(data):

        # 消除重复项目
        print('去除重复数据')
        data.drop_duplicates('订单号',inplace=True)


        # 初步处理

        print('活动产品 初步处理')
        # data = data.replace("三金美肤面膜 缓解过敏 修复护理|三金美肤面膜 维稳修护 强化屏障", "三金护肤面膜 维稳修护 强化屏障", regex=True)
        # patt = '三金补水面膜 镇静维稳 深层补水\\(补水\\)|三金美肤面膜 美白功效 健康肤色\\(美肤\\)|三金护肤面膜 维稳修护 强化屏障\\(护肤\\)|三金水光针\\(水光针\\)'
        # data['商品名'] = data['订单详情'].str.extract('(?P<商品名>%s)' % patt, expand=False).str.strip()
        #  X 1 = ￥138
        data['商品名'] = data['订单详情'].str.replace("\sX\s\d+\s=\s[￥$]\d+(?=$)","",regex=True)

        data = pd.concat([data['用户信息'].str.extract("""
                (?<=下单人：)(?P<收件人>[^\n]+)
                \s+手机：(?P<联系方式>[^\n]+)
                \s+收货地址：(?P<收货地址>[^\n]+)""", flags=re.S | re.X),data],axis=1)

        # 采用商品名匹配
        data = pd.merge(data, free_goods_map, on='商品名', how='left')

        del data['商品名']
        data = pd.merge(data,sku_goods[['商品ID','goods_type','规格', '货品编号','单位','单价','商品名','发货商']],on="商品ID")

        # 消除已经获取的数据
        print('去除已经获取的数据')

        data['key'] = data['订单号'] + "-" + data['商品ID']
        data['key'] = data['key'].apply(dup_order)
        data.dropna(subset=['key'],inplace=True)


        data['支付金额'] = 0



    free_data = data


    # 获取商城订单
    # # 同步
    # l = []
    # for order in qm.gen_orders("original",order_status=1):
    #     l.append(order)

    # data = pd.DataFrame(l)


    # 异步
    start_time('original_get_orders')
    data = qm.async_get_orders('original', 1, coroutine_max=100)
    print('-->free 耗时:%s' %(end_time('original_get_orders')))


    if len(data):

        print('去除重复数据')
        data.drop_duplicates('订单号',inplace=True)

        data = pd.concat([data['用户信息'].str.extract("""
                (?<=下单人：)(?P<收件人>[^\n]+)
                \s+手机：(?P<联系方式>[^\n]+)
                \s+收货地址：(?P<收货地址>[^\n]+)""", flags=re.S | re.X),data],axis=1)
        data = data.replace({"支付金额": {"￥": ""}}, regex=True).fillna({"支付金额": 0})

        data['支付金额'] = data['支付金额'].astype(int)

        # 拆分为原子
        data = data.drop(columns='订单详情').join(data['订单详情'].str.split('\n',expand=True).stack().reset_index(level=1, drop=True).rename("详情"))


        data = pd.concat([data[['订单号', '收件人','联系方式','收货地址', '用户信息','下单时间','备注','支付金额','支付时间']], data['详情'].str.extract(
        """
        (?P<商品名>.+?)(?=（规格[：:])（
        规格[：:](?P<规格>.+?)(?=[，,]商品ID[：:])
        [，,]商品ID[：:](?P<商品ID>.+)）\sX(?P<数量>\s\d+)""",flags=re.X)],axis=1)

        del data['商品名']
        data = pd.merge(data,sku_goods[['商品ID','goods_type', '货品编号', '单位', '单价','商品名','发货商']],on="商品ID")
        data['数量'] = data['数量'].astype(int)
        data['支付金额'] = data['数量'] * data['单价']   

        print('去除已经获取的数据')


        data['key'] = data['订单号'] + "-" + data['商品ID']

        data['key'] = data['key'].apply(dup_order)
        data.dropna(subset=['key'],inplace=True)



    original_data = data

    data = pd.concat([original_data, free_data])
    if len(data) == 0:
        print('无所需数据')
        sys.exit()


    # 存储订单信息
    save_dir = r"D:\Downloads\QHJ_MALL"
    save = SaveXl(save_dir)
    save(data,"订单")



    # 读取导出信息
    order_path, lt_time = get_new_file_path(EXPORT_DIR,ORDER_DATE_PATT)
    fm_lt_time = lt_time.strftime(DATE_FORMAT)

    print('读取 %s' %order_path)


    data = pd.read_excel(order_path, converters={"订单号":str})


    data['订单号'] = data['订单号'].astype(str)
    data['联系方式'] = data['联系方式'].astype(str)
    data = OrderInMiddleware(data)()

    data['导出订单时间'] = lt_time

    print('>>>>系统字段统一为本地字段')
    data.rename(columns=FIELDS_SLM_DIC,inplace=True)

    for filed in ['发货商', '发货商ID']:
        if filed in data:
            del data[filed]

    # 获取供应商
    print('>>>>连接供应商信息')
    data = pd.merge(data,commodity_df,how='left',on='商品ID')

    # In[4]:

    """
    分离更新 还是 插入的数据
    """

    # 存储新订单信息

    fields =  ["订单号","商品ID","货品编号",'供应商','商品名','数量','规格','单位','收件人','收货地址','联系方式','备注','发货商']

    new_order_df = data.copy()
    if len(new_order_df):
        print("存储订外发单信息")
        new_order_path = os.path.join(NEW_ORDER_BAK_DIR,"订单 %s.xlsx" %(fm_lt_time))
        print('>>>>备份')
        new_order_df.to_excel(new_order_path)

    new_order_df_r = new_order_df[fields]

    print()


    # In[10]:


    print('存储新订单 %s' %NEW_ORDER_SAVE_DIR)
    odo = OrderOutMiddleware(new_order_df_r,"发货商")
    files_info = {}
    for d_plat in new_order_df_r['发货商'].unique():
        temp = odo.out(d_plat)
        file_name = "趣领_%s_新订单 %s.xlsx" %(d_plat,fm_lt_time)
        file_path = os.path.join(NEW_ORDER_SAVE_DIR,file_name)
        
        print('>>>>正在存储 %s' %(file_name))
        files_info[d_plat] = file_path
        temp.to_excel(file_path,index=False,sheet_name="新订单")    
    print("新订单存储完成\n")




    # In[11]:
    macro_path = BEAUTY_VBA_PATH
    macro_name = "美化.xlsm!bty"
    mo = Macro(visible=EXCEL_VISIBLE)
    mo.name = macro_name
    mo.open(macro_path)

    for d_plat,file_path in files_info.items():

        macro_params = (file_path, d_plat,r"新订单|已发未回",)
        mo(params = macro_params)

    mo.close()






    # macro_path = BEAUTY_VBA_PATH
    # macro_name = "美化.xlsm!beautify"
    # macro_params = (r"E:\qhj\奇货居\work\外发订单\新订单\|D:\奇货居\work\外发订单\新订单\|D:\奇货居\work\外发订单\已发未收\\",
    #     r"(?:新订单|已发未回订单)(?= 20\d{2}(?:-\d{1,2}){2}\D+?\d{1,2}(?:_\d{1,2}){1,2}\.xlsx$)",
    #     r"新订单|已发未回",
    #     "外发订单"
    #     )


    # mo = Macro(visible=EXCEL_VISIBLE)
    # mo.open(macro_path)
    # mo(name=macro_name,params = macro_params)
    # mo.close()

    print("%0.3fs\n" %end_time('handle_order'))


if __name__ == "__main__":
    run()