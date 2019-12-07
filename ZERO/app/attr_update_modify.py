import sys
from pprint import pprint
import json
sys.path.append(r"D:\往期\QHJ\ZERO")
import requests
from tools import *

mg = MallGoods(MALL_KEY)


with open('test.json','r',encoding='utf-8') as f:
    js = json.load(f)


for data in js:

    mg.set_attr(data)





