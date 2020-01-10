import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
import os
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pymysql
import pandas as pd
from tools import *
start_time('update_goods')

mg = MallGoods(MALL_KEY)

conn = pymysql.Connect(**MYSQL_MALL_DIC)
cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute('select * from goods_class')
goods_class = pd.DataFrame(cursor.fetchall())
goods_class_dic = dict(zip(goods_class['class_name'],goods_class['class_id']))



goods_path = r"D:\奇货居\素材\商城图片素材\商品信息.xlsx"


file_o = pd.ExcelFile(goods_path)


goods_df = file_o.parse("商品详情",)
# not_uploaded_df = file_o.parse('未上传')

not_uploaded_df = file_o.parse('SPU')[:2]
not_uploaded_df.loc[0,'goods_id'] = 27
not_uploaded_df.loc[1,'goods_id'] = 31



# 上传新商品 图片 修改属性
print('>>>>修改属性')
for index,row in not_uploaded_df.iterrows():
    goods_id = row['goods_id']
    img_dir = os.path.join(row['img_dir'],"轮播")
    mg.up_imgs(goods_id,img_dir,"goods_slide")

    img_dir = os.path.join(row['img_dir'],"详情")
    
    mg.up_imgs(goods_id,img_dir,"goods_info")
    
    
    
    
    # 修改 goods 描述信息
    data = {
            "goods_name": row['商品名简称'],
            "class_id": goods_class_dic[row['系统分类']],
            "goods_info": row['商品名简称'],
            "goods_id": goods_id,
    }
    mg.set_goods(data)
    
    # 上架
    mg.set_shelf(goods_id,1)
    
    # 设置 goods 属性
    data = {
        "goods_id":goods_id,
        "sort":0,
        'send_price':15,
        'goods_price':row['市场价']
    }

    mg.set_good_opt(data)




# 规格 细节属性

print('>>>>修改商品细节属性')
not_uploaded_free_df = not_uploaded_df[not_uploaded_df['goods_type'] != 'free']
rename_dic = {
    "商品ID":"attr_goods_code",
    "规格":"attr_name",
    '售价':"attr_price",
    '单位' :"attr_unit",
    "市场价" :'attr_old_price'
}
goods_df_r = goods_df[['商品ID','规格','售价','单位','市场价','attr_stock','SPUID']]

not_uploaded_free_df = pd.merge(not_uploaded_free_df[['SPUID','goods_id']],goods_df_r,on='SPUID')


not_uploaded_free_df.rename(columns=rename_dic,inplace=True)
not_uploaded_free_df['attr_stock'][not_uploaded_free_df['attr_stock'].isnull()] = 500

mg.set_attrs(not_uploaded_free_df)

print("%0.3fs\n" %end_time("update_goods"))
