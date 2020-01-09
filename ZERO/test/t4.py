import re
import os
from random import randint
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
sys.path.append(r"E:\dataparse\Python_DATA_PARSE\QHJ\ZERO")
from pyquery import PyQuery as pq
import requests
from tools import *


url = 'https://app0001.yrapps.cn/admin/Goodclass/goodClass'
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "cookie": "PHPSESSID=%s" %MALL_KEY,
    "pragma": "no-cache",
    "referer": "https://app0001.yrapps.cn/admin/index/index",
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4000.3 Safari/537.36",
}


rep = requests.get(url,headers=headers)
doc = pq(rep.text)

tbody td img[goods_id]