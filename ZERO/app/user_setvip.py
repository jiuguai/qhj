import sys
sys.path.append(r"D:\往期\QHJ\ZERO")

sys.path.append(r"F:\QHJ\qhj\ZERO")

import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tools import *

engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(**MYSQL_MALL_DIC),encoding='utf-8')

Session = sessionmaker(bind=engine)
session = Session()

import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index
# from sqlalchemy.exc import IntegrityError
Base = declarative_base()


class Users(Base):
    __tablename__ = 'user'                #表名称
    openid = Column(String(50), primary_key=True) # primary_key=True设置主键
    name = Column(String(20), ) #index=True创建索引， nullable=False不为空。
    phone = Column(String(11))
    province = Column(String(20))
    city = Column(String(40))






path_file = r"C:\Users\qhj01\Desktop\毛总客户.xlsx"
file_obj = pd.ExcelFile(path_file)
print(file_obj.sheet_names)
data = file_obj.parse('会员设置',index=False)
print(data.columns)

result = session.execute("select openid from user").fetchall()
openid_set = set([t[0] for t in result])





url = "https://app0001.yrapps.cn/admin/user/add_user_member.html"

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-length": "196",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": "PHPSESSID=%s" %MALL_KEY,
    "origin": "https://app0001.yrapps.cn",
    "pragma": "no-cache",
    # "referer": "https://app0001.yrapps.cn/admin/user/user_member/openid/oDMUF5nBcsojtcOTAfJnLb0Bh0Do.html",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",

}




activate_url = "https://app0001.yrapps.cn/admin/user/member_activate.html"


activate_headers = {
    
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-length": "46",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": "PHPSESSID=%s" %MALL_KEY,
    "origin": "https://app0001.yrapps.cn",
    "referer": "https://app0001.yrapps.cn/admin/User/userMemberList?page=4",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4000.3 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

# level
#   0:白户
#   1:VIP
#   2:VVIP

own_set = set(data['openid']) - openid_set
data = data[data['openid'].isin(own_set)]
# ['name', 'province', 'phone', 'city', 'openid']
for index, row in data.iterrows():
  
    data = {
        "name": row['name'],
        "expire_time": "2021-01-16",
        "level": "2",
        "phone": row['phone'],
        "province":row['province'],
        "city": row['city'],
        "openid": row['openid'],

    }

    activate_data = {
        "openid": row['openid'],
        "is_shelf": 1
    }
    rep = requests.post(url, headers=headers, data=data)
    js = rep.json()
    js.update({'openid':row['openid'],'operation':'设置VIP'})
    print(js)

    rep = requests.post(activate_url, headers=activate_headers, data=activate_data)
    js.update({"openid":row['openid'],'operation':'激活'})
    print(js)


    row_data = row.to_dict()
    print(row_data)
    print('-'*20)
    obj = Users(**row_data)
    session.add(obj)
    try:

        session.commit()
    except :
        session.rollback()
        

session.close()