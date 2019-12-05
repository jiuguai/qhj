import requests
from retrying import retry
url = "https://app0001.yrapps.cn/"
a = 0
class T(Exception):
	pass
def gen_retry(try_max):
	
	def outer(func):
		
		def inner( *args, **kargs):
			expt_num = kargs.pop("expt_num",0)
			faild = True
			try:

				return func(*args, **kargs)
			except T:
				pass
			else:
				faild = False

			finally :
				expt_num += 1	
				
				if faild & expt_num != try_max:
					kargs['expt_num'] = expt_num
					return inner( *args, **kargs)
				
		return inner
	return outer

# stop_max_attempt_number
# @gen_retry(3)
MAX_TRY = 3
@retry(stop_max_attempt_number=MAX_TRY)
def t():
	global a
	a += 1
	print(a)
	rep = requests.get(url, timeout=0.122)
	return rep.text
	

print(t())