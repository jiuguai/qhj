import sys
import os
import importlib
from pprint import pprint
import queue

# pprint(dict(os.environ).get("SCRAPY_SETTINGS_MODULE"))
# print(sys.modules)
print(os.path.dirname(__file__))
# sys.path.append(os.path.split(os.path.dirname(__file__))[0])
print(sys.path)
import_name = "jianshuv2.middlewares.Jianshuv2DownloaderMiddleware"
module_name, obj_name = import_name.rsplit('.',1)
print(module_name, obj_name)
# module = __import__(module_name, None, None, [obj_name])
module = importlib.import_module(module_name)
print(module)
print(getattr(module,obj_name))




class PQ():
	def __init__(self,priority,class_name):
		self.priority = priority
		self.class_name = class_name
	def __lt__(self,other):
		return self.priority < other.priority
	def __eq__(self,other):
		return self.priority == other.priority

que = queue.PriorityQueue()
q = {"a":3,"b":2,"c":1}
que.put(PQ(5,"a"))
que.put(PQ(2,"b"))
que.put(PQ(1,"c"))
que.put(PQ(3,'d'))
que.put(PQ(3,'e'))
l = []
while not que.empty():
	l.append(que.get().class_name)

print(l)
