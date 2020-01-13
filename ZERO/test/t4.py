import re
import os
from random import randint
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
sys.path.append(r"F:\QHJ\qhj\ZERO")
from pyquery import PyQuery as pq
import requests
from tools import *


url = 'https://app0001.yrapps.cn/admin/good/edit_good.html'
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",

    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": "PHPSESSID=%s" %MALL_KEY,
    "origin": "https://app0001.yrapps.cn",
    "pragma": "no-cache",
    "referer": "https://app0001.yrapps.cn/admin/good/good_edit/goods_id/27.html",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4000.3 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

data = {
    "goods_name": "zero",
    "class_id": "1",
    "goods_info": "zero",
    "goods_id": "27",
}

rep = requests.post(url,data=data,headers=headers)

print(rep.json())