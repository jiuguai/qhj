
from celery.result import AsyncResult
from t4 import add,cel
# cid = add.delay(4,5)
# print("---",cid)
result = AsyncResult(id="0de08490-f3df-43cf-8fcd-b7495cd324c",app=cel)


print(result.get())