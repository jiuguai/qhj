from aiohttp import ClientSession
import asyncio
from pyquery import PyQuery as pq



url = "https://app0001.yrapps.cn/admin/User/userlist?page=2"

headers = {
    
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    # "cookie": "PHPSESSID=9g1juso7sb2l30fm5b6m4iutoc",
    "pragma": "no-cache",
    "referer": "https://app0001.yrapps.cn/admin/User/userlist",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4021.2 Safari/537.36",
}
cookies = {'PHPSESSID','9g1juso7sb2l30fm5b6m4iutoc'}
print(1)

async def t():
    async with ClientSession() as session:
        async with session.get(url,headers=headers) as resp:
            print(resp.status)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(t())