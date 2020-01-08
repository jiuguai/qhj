import time

import celery
broker = "redis://127.0.0.1:6379/0"

backend = "redis://127.0.0.1:6379/0"

cel = celery.Celery('test',broker =broker,backend=backend)


@cel.task
def add(x,y):
	# print(x+y)
	return x +y 
