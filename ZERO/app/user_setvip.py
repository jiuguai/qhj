import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
sys.path.append(r"E:\dataparse\Python_DATA_PARSE\QHJ\ZERO")
import requests


from tools import *
url = "https://app0001.yrapps.cn/admin/user/add_user_member.html"


headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "content-length": "196",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": "PHPSESSID=%s" %MALL_KEY,
    "origin": "https://app0001.yrapps.cn",
    "pragma": "no-cache",
    "referer": "https://app0001.yrapps.cn/admin/user/user_member/openid/oDMUF5nBcsojtcOTAfJnLb0Bh0Do.html",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",

}


# level
#   0:白户
#   1:VIP
#   2:VVIP
data = {
    "name": "杨晗",
    "expire_time": "2020-12-19",
    "level": "1",
    "phone": "15898538422",
    "province": "湖南",
    "city": "长沙市",
    "openid": "oDMUF5nuF8bxZga9I2shOqtoNgA0",
}

file_path = ""



rep = requests.post(url, headers=headers, data=data)
print(rep.json())