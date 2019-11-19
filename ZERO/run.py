
import logging


logger = logging.getLogger("九怪")
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('test.log',encoding='utf-8',mode='a') 

# 再创建一个handler，用于输出到控制台 
ch = logging.StreamHandler() 
formatter = logging.Formatter('%(asctime)s<%(module)s>-%(levelname)s-%(lineno)s: %(message)s')
fh.setLevel(logging.DEBUG)
ch.setLevel(logging.ERROR)

fh.setFormatter(formatter) 
ch.setFormatter(formatter) 
# logger.addHandler(fh) #logger对象可以添加多个fh和ch对象 
logger.addHandler(ch) 

logger.debug('logger debug 就是干') 
logger.info('logger info 就是干') 
logger.warning('logger warning 就是干') 
logger.error('logger error 就是干') 
logger.critical('logger critical 就是干')
