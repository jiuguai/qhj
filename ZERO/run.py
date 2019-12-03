import sys
sys.path.append(r"D:\往期\奇货居\ZERO")

from tools import *


x = get_duplicated_field([1,2,1,3,4,2])
print(x)



for i in range(15):
    print(i)



#import hashlib

#import pandas as pd

#l = []
#for i in range(1,26):
#	md5 = hashlib.md5()
#	md5.update(str(i).encode())
#	l.append(md5.hexdigest())
#s = pd.Series(l)

# import logging


# logger = logging.getLogger("九怪")
# # 创建一个handler，用于写入日志文件
# fh = logging.FileHandler('test.log',encoding='utf-8',mode='a') 

# # 再创建一个handler，用于输出到控制台 
# ch = logging.StreamHandler() 
# formatter = logging.Formatter('%(asctime)s<%(module)s>-%(levelname)s-%(lineno)s: %(message)s')
# fh.setLevel(logging.DEBUG)
# ch.setLevel(logging.ERROR)

# fh.setFormatter(formatter) 
# ch.setFormatter(formatter) 
# # logger.addHandler(fh) #logger对象可以添加多个fh和ch对象 
# logger.addHandler(ch) 

# logger.debug('logger debug 就是干') 
# logger.info('logger info 就是干') 
# logger.warning('logger warning 就是干') 
# logger.error('logger error 就是干') 
# logger.critical('logger critical 就是干')
