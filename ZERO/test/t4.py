import os
import sys
import hashlib
sys.path.append(r"D:\往期\QHJ\ZERO")

import datetime
import hashlib
from tools import MallGoods,MALL_KEY


mg = MallGoods(MALL_KEY)

import requests
from pyquery import PyQuery as pq

import re


goods_id = 26
img_dir = r'D:\ZERO_TEMP\img\test\Huawei Mate 30\轮播'
mg.up_imgs(goods_id,img_dir,"goods_slide")

img_dir = r'D:\ZERO_TEMP\img\test\Huawei Mate 30\详情'
mg.up_imgs(goods_id,img_dir,"goods_info")
