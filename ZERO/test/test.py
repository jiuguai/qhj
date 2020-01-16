import re
import asyncio
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")

from aiohttp import ClientSession, ClientTimeout, TCPConnector
import requests
from pyquery import PyQuery as pq

from tools import *

      


async def get_order(data, order_type, gen, **kargs):
    url = "https://app0001.yrapps.cn/admin/Order/orderList"

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
        print('request %s %s page' %(order_type,page))

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
                l = [[td.text().strip() for td in tr('td').items()] for tr in doc('tbody tr').items()]

                data.extend(l)
            
def _get_order_init(order_type,**kargs):
    url = "https://app0001.yrapps.cn/admin/Order/orderList"

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

    params = {
        "order_status": kargs.get("order_status", 0),
        "order_time": kargs.get("order_time", ""),
        "order_id": kargs.get("order_id", ""),
        "order_type": order_type,
        "page": 1,
    }
    print('first request %s %s page' %(order_type,1))
    resp = requests.get(url,params=params,headers=headers)
    text = resp.text
    doc = pq(text)
    # data = []
    # l = [item.text() for item in doc('tbody tr td:nth-child(2)').items()]

    data = []
    l = [[td.text().strip() for td in tr('td').items()] for tr in doc('tbody tr').items()]

    data.extend(l)

    columns = [item.text() for item in doc('thead tr th').items()]


    total = doc('.pagination li:nth-last-child(2)').text()
    total = int(total) if total else 0
    return total, columns, data


def async_get_orders(order_type, order_status, coroutine_max=100,**kargs):
    start_time('s')
    # 请求类型 0 表示所有订单 1 未发货  2 已发货
    # 3 已完成 4 申请退款 5 退款成功  10 未支付
    order_status = order_status
    order_type = order_type
    COROUTINE_MAX = coroutine_max
    total_page, columns, data = init(order_type,order_status=order_status, **kargs)

    print("comfirm pagination total %s" %total_page)


    loop = asyncio.get_event_loop()
    
    tasks = []

    gen = iter(range(2,total_page+1))
    for coroutine in range(COROUTINE_MAX):
        tasks.append(get_order(data, order_type, gen, order_status=order_status, **kargs))

    loop.run_until_complete(asyncio.wait( tasks))
    print('--> %s' %end_time('s'))
    df = pd.DataFrame(data, columns=columns)
    print('--> %s 条' %len(data))
    df.drop_duplicates('订单号',inplace=True)
    return df
    # print(data)
    # df.drop_duplicates('订单号',inplace=True)
    # df.to_excel(r"C:\Users\qhj01\Desktop\zero.xlsx",index=False)

if __name__ == '__main__':
    qm = QHJMall(MALL_KEY)
    start_time('s')

    df = qm.async_get_orders('free',0, coroutine_max=100)
    print('-->耗时:%s' %(end_time('s')))
    df.to_excel(r"C:\Users\qhj01\Desktop\zero.xlsx",index=False)