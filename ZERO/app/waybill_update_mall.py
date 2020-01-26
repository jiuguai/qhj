import re
import sys
import datetime
sys.path.append(r"D:\往期\QHJ\ZERO")
sys.path.append(r"F:\QHJ\qhj\ZERO")
from pyquery import PyQuery as pq
import requests
from urllib.parse import urlencode,parse_qs
import numpy as np
import pandas as pd
import redis

import json
from tools import *

def run():

	qm = QHJMall(MALL_KEY)
	conn = redis.Redis(**REDIS_MALL_ORDER_DIC)

	# 需要整合
	# 
	# 
	# 
	wb_up_dir = os.path.join(NEW_ORDER_SAVE_DIR,"反馈数据")
	l = []
	for file_name in os.listdir(wb_up_dir):
	    file_path = os.path.join(wb_up_dir, file_name)

	    if not file_name.startswith("~$") and os.path.isfile(file_path):
	        

	        print(file_path)

	        data = read_xl(file_path,'订单号',converters={"订单号":str,'运单号':str})
	     
	        
	        l.append(data)

	data = pd.concat(l,sort=False)


	data.dropna(subset=['运单号'],inplace=True)
	data.reset_index(drop=True,inplace=True)

	print('可更新数据:%s条' %(len(data)))


	for i,row in data.iterrows():
	    qm.set_wb(row['订单号'],row['快递公司'],row['运单号'])


if __name__ == '__main__':
    run()
