import asyncio
from collections import Counter

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from pyquery import PyQuery as pq


url = "https://app0001.yrapps.cn/admin/User/userlist?page=%s"

headers = {
    
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "cookie": "PHPSESSID=9g1juso7sb2l30fm5b6m4iutoc",
    "pragma": "no-cache",
    "referer": "https://app0001.yrapps.cn/admin/User/userlist",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4021.2 Safari/537.36",
}
# cookies = {'PHPSESSID','9g1juso7sb2l30fm5b6m4iutoc'}
# print(1)
# 

"""方案一


"""


data = []
async def user(page):
    timeout = ClientTimeout(total=15)
    async with ClientSession(timeout=timeout) as session:
        async with session.get(url %page,headers=headers) as resp:
            print(page)
            text = await resp.text()
            doc = pq(text)
            tds = doc('tbody tr td:nth-child(3)')
            l = []
            for td in tds.items():
                l.append(td.text())
            data.extend(l)
            


    
if __name__ == "__main__":


    loop = asyncio.get_event_loop()
    tasks = []
    for page in range(1,25):
        tasks.append(user(page))
    loop.run_until_complete(asyncio.wait(tasks))
    user_counter = Counter(data)
    print(user_counter.most_common(5))
    print(data)
    


"""""

方案二
"""

# data = []

# async def _user(session, page):
#     async with session.get(url %page,headers=headers) as resp:
    
#         print(page)
#         text = await resp.text()
#         doc = pq(text)
#         tds = doc('tbody tr td:nth-child(3)')
#         l = []
#         for td in tds.items():
#             l.append(td.text())
#         data.extend(l)




# async def user(total):
#     timeout = ClientTimeout(total=15)
#     conn = TCPConnector(limit=20)
#     async with ClientSession(connector=conn,timeout=timeout) as session:

#         await asyncio.gather(*[asyncio.ensure_future(_user(session, page)) for page in range(1,total+1)])

    
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(asyncio.gather(user(33)))

#     user_counter = Counter(data)
#     print(user_counter.most_common(5))
#     print(data)