# -*- coding: utf-8 -*-
"""
Created on  2019-12-04 16:46:35

@author: zero
"""
# In[导包]

import os
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import pymysql
from pyquery import PyQuery as pq
import requests
from sqlalchemy import create_engine

from tools import *

# In[]
start_time('get_orders')
phpsessid = "ik9uh45jlsaih896qopsupoa3s"

url = "https://app0001.yrapps.cn/admin/order/send_order.html"

headers = {
	"accept": "*/*",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
	"cache-control": "no-cache",
	"content-length": "57",
	"content-type": "application/x-www-form-urlencoded; charset=UTF-8",
	"cookie": "PHPSESSID=ik9uh45jlsaih896qopsupoa3s",
	"origin": "https://app0001.yrapps.cn",
	"pragma": "no-cache",
	"referer": "https://app0001.yrapps.cn/admin/order/order_delivery/order_id/19113010050544.html",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-origin",
	"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
	"x-requested-with": "XMLHttpRequest",
}

data = {
	"express_info": "xxx",
	"express_id": "xxx",
	"order_id": "19120154971011"
	}
rep = requests.post(url, headers=headers, data=data)

js = rep.json()

if js['code'] == 200:
	print('修改成功')
else:
	print('修改失败')



