import re
import asyncio
from collections import Counter

import sys
sys.path.append(r"D:\往期\QHJ\ZERO")

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from pyquery import PyQuery as pq
import requests
from tools import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index

def run():
    # from sqlalchemy.exc import IntegrityError
    engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'.format(**MYSQL_MALL_DIC),encoding='utf-8')

    Base = declarative_base()
    sql_session = sessionmaker(bind=engine)
    ss = sql_session()


    class User(Base):
        __tablename__ = 'user'                #表名称
        openid = Column(String(50), primary_key=True) # primary_key=True设置主键
        name = Column(String(20), ) #index=True创建索引， nullable=False不为空。
        phone = Column(String(11))
        province = Column(String(20))
        city = Column(String(40))
        status = Column(String(20))
        level = Column(String(10))
        nickname = Column(String(20))

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "cookie": "PHPSESSID=%s" %MALL_KEY,
        "pragma": "no-cache",
        "referer": "https://app0001.yrapps.cn/admin/User/userMemberList",
        "sec-fetch-dest": "iframe",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4021.2 Safari/537.36",
    }

    async def vuser(url,data):
        async with ClientSession() as session:
            print('request %s' %url)
            async with session.get(url,headers=headers) as resp:
                
                if resp.status == 200:
                    text = await resp.text()
                    doc = pq(text)
                    for tr in doc("tbody tr").items():
                        l = []
                        for td in tr('td').items():
                            l.append(td.text().strip())


                        openid = tr('.td-status [onclick]').attr("onclick")
                        if openid:
                            l.append(com.search(openid).group(1))
                        else:
                            l.append("")

                        data.append(l)
                else :
                    print('>>>> request is faild %s' %url)

    def init(url):
        data = []
        print('first request %s' %url)
        resp = requests.get(url,headers=headers)
        doc = pq(resp.text)
        columns = [item.text() for item in doc("thead tr th").items()]
        columns.append("openid")
        for tr in doc("tbody tr").items():
            l = []
            for td in tr('td').items():
                l.append(td.text().strip())


            openid = tr('.td-status [onclick]').attr("onclick")
            if openid:
                l.append(com.search(openid).group(1))
            else:
                l.append("")

            data.append(l)
        total = doc('.pagination li:nth-last-child(2)').text()
        total = int(total) if total else 0
        return total ,columns, data

    com = re.compile('\'(?P<openid>.+?)\'')
    if __name__ == '__main__':
        url = "https://app0001.yrapps.cn/admin/User/userMemberList?page=%s"
        start_time('s')
        total_page, columns, data = init(url %1)


        loop = asyncio.get_event_loop()

        tasks = []
        for page in range(2,total_page+1):
            tasks.append(vuser(url %page,data))
        loop.run_until_complete(asyncio.wait(tasks))
        df = pd.DataFrame(data, columns=columns)
        df = df[['openid',"呢称","手机",'会员等级','状态']]
        re_col = {
            "呢称":"nickname",
            "手机":"phone",
            "会员等级":"level",
            "状态":"status",

        }
        ss.execute("delete from user")
        df.rename(columns=re_col,inplace=True)
        for index, row in df.iterrows():
            ss.add(User(**row.to_dict()))


        ss.commit()
        # print(df)
        
        print('%s' %end_time('s'))


if __name__ == '__main__':
    run()
