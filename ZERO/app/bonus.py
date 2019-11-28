#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")

import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine

from tools import *

# In[变量]

# 分红关系
commission_dic = {
    "VIP":20,
    "VVIP":50
}

save = SaveXl(r'D:\ZERO_TEMP')
suf = save.suf
# In[读取数据 初步处理]
file_path = r"C:\Users\qhj01\Desktop\用户模拟数据.xlsx"

df = pd.read_excel(file_path)
df['reg_time'] = pd.to_datetime(df['reg_time'])
df.sort_values('reg_time',inplace=True)


# In[调整reg_id]
df.reset_index(drop=True,inplace=True)
df.index.name = 'reg_id'
df.index += 1
df.reset_index(inplace=True)

# I[标记新增ID]

# In[添加所需要字段]:
data = df.set_index('reg_id',drop=False     )
data['grandfather_id'] = 0
data['grandfather'] = None
data['level'] = 1
data['root'] = None
data['root_name'] = None
data['二级佣金'] = 0
data['三级佣金'] = 0
data['无限极佣金'] = 0




data['root'][data['parent_id'] == 0] = data[data['parent_id'] == 0]['reg_id']
data['root_name'][data['parent_id'] == 0] = data[data['parent_id'] == 0]['user_name']




# In[处理多级数据]:


for index,row in data.iterrows():
    parent_id = row['parent_id']
    state = row['state']
    commission = commission_dic.get(state,0)
    

    # 二级
    if parent_id:

        data.loc[index,'level'] += data.loc[parent_id,'level']
        data.loc[index,'root'] = data.loc[parent_id,'root']
        data.loc[index,'root_name'] = data.loc[parent_id,'root_name']
        
        data.loc[parent_id,'二级佣金'] +=  commission
        data.loc[parent_id,'无限极佣金'] +=  commission
        
        parent_id = data.loc[parent_id,'parent_id']
    
    # 三级
    if parent_id:
        data.loc[parent_id,'三级佣金'] += commission
        data.loc[parent_id,'无限极佣金'] +=  commission
        
        data.loc[index,'grandfather_id'] =  parent_id
        data.loc[index,'grandfather'] =  data.loc[parent_id,'user_name']
        
        parent_id = data.loc[parent_id,'parent_id']

    while parent_id:
        data.loc[parent_id,'无限极佣金'] +=  commission
        parent_id = data.loc[parent_id,'parent_id']

        


# In[保存多级数据]:
save(data,'处理后的数据')


# In[处理三级数据]:


temp = data[['state','reg_id', 'user_name', 'parent_id', 'parent_name', 'grandfather', 'grandfather_id']]. dropna().rename(columns={"user_name":"三级用户名",
                         'state':"三级用户等级",
                         'parent_name':"二级用户名"})
temp['可抽取佣金'] = temp['三级用户等级'].apply(lambda  x:commission_dic.get(x,0))



# In[存储三级数据]:

save.suf = ""
save_dir = r"C:\Users\zero\Desktop\T\需要发送的三级名单"
for (grandfather,grandfather_id),t in temp.groupby(['grandfather','grandfather_id']):
    t=  t[['二级用户名','三级用户名','三级用户等级','可抽取佣金']].sort_values('二级用户名')

    save(t, r'T\%s_%s' %(grandfather_id,grandfather))

    







