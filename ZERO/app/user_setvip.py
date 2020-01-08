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




activate_url = "https://app0001.yrapps.cn/admin/user/member_activate.html"


activate_headers = {
    
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-length": "46",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": "PHPSESSID=%s" %MALL_KEY,
    "origin": "https://app0001.yrapps.cn",
    "referer": "https://app0001.yrapps.cn/admin/User/userMemberList?page=4",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4000.3 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

# level
#   0:白户
#   1:VIP
#   2:VVIP
data = {
    "name": "冯国鑫",
    "expire_time": "2021-01-03",
    "level": "2",
    "phone": "13142099997",
    "province": "湖南",
    "city": "长沙市",
    "openid": "oDMUF5nBir2ljeE4GmwWfZR3hXAo",
}

activate_data = {
    "openid": "oDMUF5nBir2ljeE4GmwWfZR3hXAo",
    "is_shelf": 1
}
rep = requests.post(url, headers=headers, data=data)
print(rep.json())

rep = requests.post(activate_url, headers=activate_headers, data=activate_data)
print(rep.json())