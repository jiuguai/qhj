from pprint import pprint

import requests

# url = 'http://api.map.baidu.com/geocoding/v3/?address=北京市海淀区上地十街10号&output=json&ret_coordtype=gcj02ll&ak=pKthM9TxiqPsGx81IAwlkVuGRphmwdDR'


# rep = requests.get(url)
# pprint(rep.json())

# \u4f9b\u5e94\u5546

FIELDS_SLM_DIC = {
	"a" : 1
}

# 本地字段 映射 系统字段

FIELDS_LSM_DIC = {v:k for k, v in FIELDS_SLM_DIC.items()}

print(FIELDS_LSM_DIC)