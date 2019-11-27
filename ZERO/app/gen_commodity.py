#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
sys.path.append(r"D:\往期\奇货居\ZERO")

import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine

from tools import *




# In[2]:



start_time("商品详情")


sp_prefix = "商品详情"
gg_prefix = "规格_交易详情"


# In[3]:


shipper_df = pd.read_excel(os.path.join(COMMODITY_BASE_DIR,"发货商详情.xlsx"))
shipper_df.dropna(subset=["发货商ID"],inplace=True)


# In[4]:


data_l = []


for index, shipper_row in shipper_df.iterrows():
    pro_dir = os.path.join(COMMODITY_BASE_DIR,shipper_row['发货商目录'])
    gys_path = os.path.join(pro_dir,"供应商详情.xlsx")
    gys_df = pd.read_excel(gys_path)
    gys_df.dropna(subset= [ '供应商ID'] ,inplace=True)
    print( shipper_row['发货商目录'])
    for index,gys_row in gys_df.iterrows():
        gys_dir = gys_row['供应商目录']
        sp_path = os.path.join(pro_dir,gys_dir,"%s_%s.xlsx" %(sp_prefix,gys_dir))

        # ['商品名', '商品目录名', '商品编码','类别']
        sp_df = pd.read_excel(sp_path)
        sp_df.dropna(inplace=True,subset=["商品编码"])
        print("     %s" %gys_dir)

        for index,sp_row in sp_df.iterrows():
            sp_dir = sp_row['商品目录名']
            print("         %s" %sp_dir)
            gg_path = os.path.join(pro_dir,gys_dir,sp_dir,"%s_%s.xlsx" %(gg_prefix,sp_dir))
            gg_df = pd.read_excel(gg_path,sheet_name="规格")
            gg_df.dropna(subset=["商品名"],inplace=True)
            
            gg_df['发货商'] = shipper_row['发货商']
            gg_df['发货商ID'] = shipper_row['发货商ID']
            
            gg_df['供应商'] = gys_row['供应商']
            gg_df['供应商ID'] = gys_row['供应商ID']
            gg_df['商品编码'] = sp_row['商品编码']
#             r'=HYPERLINK("%s\%s\%s\%s","%s")' %(COMMODITY_BASE_DIR, shipper_row['发货商目录'], gys_dir, sp_dir, sp_row['商品名简称'])
            gg_df['商品名简称'] = r'=HYPERLINK("%s","%s")' %(sp_path, sp_row['商品名简称'])
            gg_df['商品名'] = r'=HYPERLINK("%s","' %(gg_path) + gg_df['商品名'] + '")'
            
            gg_df['商品ID'] = gg_df['发货商ID'] + gg_df['供应商ID'] + gg_df['商品编码'] + gg_df['规格编码']
            gg_df['商品ID'] = r'=HYPERLINK("%s\%s\%s\%s","' %(COMMODITY_BASE_DIR, shipper_row['发货商目录'], 
                                                                gys_dir, sp_dir) + gg_df['商品ID']+'")'
            
            
            try:
                gg_df['类别'] = sp_row['类别']
            except:
                pass
#             gg_df['相对目录'] = r'=HYPERLINK("%s\%s\%s\%s","GO")' %(COMMODITY_BASE_DIR, shipper_row['发货商目录'], gys_dir, sp_dir)
            data_l.append(gg_df)

sp_data = pd.concat(data_l)
sp_data.reset_index(drop=True,inplace=True)
 


# In[5]:


# 存储
writer = pd.ExcelWriter(os.path.join(COMMODITY_BASE_DIR,"商品信息.xlsx"))

fields = ['序号','商品ID','类别','商品名简称','商品名','单位', '规格', '规格模式', '市场价', '售价', '规格编码', '交易编码', '发货商','发货商ID','供应商', '供应商ID',
        '商品编码',  ]

add_order(sp_data[sp_data['状态'] != "下架"])[fields].to_excel(writer,index=False,sheet_name="商品详情")
add_order(sp_data[sp_data['状态'] == "下架"])[fields].to_excel(writer,index=False,sheet_name="下架商品")
writer.save()


# In[6]:





macro_path = BEAUTY_VBA_PATH
macro_name = "美化.xlsm!beautify"
macro_params = r"D:\奇货居\素材\商城图片素材\\"


mo = Macro(visible=EXCEL_VISIBLE)
mo.open(macro_path)
mo(name=macro_name,params = (macro_params,))
mo.close()


print("%0.3fs\n" %end_time("商品详情"))


# In[ ]:




