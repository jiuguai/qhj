from collections import Counter
import asyncio

from aiohttp import ClientSession,ClientTimeout,TCPConnector
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

data = []
async def t(page):

    timeout = ClientTimeout(total=60)
    async with ClientSession(timeout=timeout) as session:
        print(page)
        async with session.get(url %page,headers=headers) as resp:
            text = await resp.text()
         
            doc = pq(text)
            r = doc('tbody tr td:nth-child(3)')
            # print(r.text())
            l = []
            for item in r.items():
                l.append(item.text())
            data.extend(l)
            print(l)
            # print(dir(r))
if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    tasks = [t(page) for page in range(1,33)]
    loop.run_until_complete(asyncio.wait(tasks))
    print('---->',len(data))
    print('---->',len(set(data)))
    word_counts = Counter(data)
    print(word_counts.most_common(5))
    # print(data)