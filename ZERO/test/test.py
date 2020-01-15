import re
import asyncio
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")

from aiohttp import ClientSession, ClientTimeout, TCPConnector
import requests
from pyquery import PyQuery as pq

from tools import *

headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "cookie": "PHPSESSID=%s" %MALL_KEY,
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/index/index",
            "sec-fetch-mode": "nested-navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}       


async def get_order(data, order_type, gen, **kargs):
    url = "https://app0001.yrapps.cn/admin/Order/orderList"
    """
    params = {
        # 请求类型 0 表示所有订单 1 未发货  2 已发货
        # 3 已完成 4 申请退款 5 退款成功  10 未支付
        "order_status": kargs.get("order_status", 0),
        "order_time": kargs.get("order_time", ""), # today yesterday week month
        "order_id": kargs.get("order_id", ""), # 订单号
        "order_type": order_type,  # original free
        "page": kargs.get("page", 1),  #
    }
    """
    for page in gen:
        print('---- %s' %page)

        async with ClientSession() as session:
            params = {
                "order_status": kargs.get("order_status", 0),
                "order_time": kargs.get("order_time", ""),
                "order_id": kargs.get("order_id", ""),
                "order_type": order_type,
                "page": page,
            }
            async with session.get(url ,headers=headers,params=params) as resp:
                l = []
                text = await resp.text()
                doc = pq(text)
                l = [item.text() for item in doc('tbody tr td:nth-child(2)').items()]

                data.extend(l)
            
def init(order_type,**kargs):
    url = "https://app0001.yrapps.cn/admin/Order/orderList"
    params = {
        "order_status": kargs.get("order_status", 0),
        "order_time": kargs.get("order_time", ""),
        "order_id": kargs.get("order_id", ""),
        "order_type": order_type,
        "page": 1,
    }
    resp = requests.get(url,params=params,headers=headers)
    text = resp.text
    doc = pq(text)
    data = []
    l = [item.text() for item in doc('tbody tr td:nth-child(2)').items()]

    data.extend(l)

    columns = [item.text() for item in doc('thead tr th').items()]


    total = doc('.pagination li:nth-last-child(2)').text()
    total = int(total) if total else 0
    return total, columns, data





if __name__ == '__main__':
    start_time('s')
    
    order_type = 'free'
    COROUTINE_MAX = 20
    total_page, columns, data = init(order_type)
    print(columns)
    print(total_page)
    
    loop = asyncio.get_event_loop()
   
    tasks = []

    gen = iter(range(2,total_page+1))
    for coroutine in range(COROUTINE_MAX):
        tasks.append(get_order(data, order_type, gen))

    loop.run_until_complete(asyncio.wait( tasks))
    print('--> %s' %end_time('s'))

    print('--> %s 条' %len(data))
    print('--> %s 条' %len(set(data)))
    print(data)