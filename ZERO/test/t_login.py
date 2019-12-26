from pprint import pprint


import requests
img_url = "https://app0001.yrapps.cn/vcode?0.5584253105718886"

img_headers = {
	"accept": "image/webp,image/apng,image/*,*/*;q=0.8",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
	"cache-control": "no-cache",
	"cookie": "PHPSESSID=pllplf8btgv9apvi5ed6geqmqv",
	"pragma": "no-cache",
	"referer": "https://app0001.yrapps.cn/",
	"sec-fetch-mode": "no-cors",
	"sec-fetch-site": "same-origin",
	"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}

key = "070659"
sh_key = "pllplf8btgv9apvi5ed6geqmqv"
# imdq8fo2l0tdvav6m440uqg2r8



index_url = "https://app0001.yrapps.cn/admin/index/index"

index_headers = {
	
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
	"cache-control": "no-cache",
	"cookie": "PHPSESSID=pllplf8btgv9apvi5ed6geqmqv",
	"pragma": "no-cache",
	"referer": "https://app0001.yrapps.cn/",
	"sec-fetch-mode": "navigate",
	"sec-fetch-site": "same-origin",
	"sec-fetch-user": "?1",
	"upgrade-insecure-requests": "1",
	"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",

}



login_url = "https://app0001.yrapps.cn/admin/login/loginCheck"

login_headers = {
	"accept": "*/*",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
	"cache-control": "no-cache",
	# "content-length": "43",
	"content-type": "application/x-www-form-urlencoded; charset=UTF-8",
	"cookie": "PHPSESSID=pllplf8btgv9apvi5ed6geqmqv",
	"origin": "https://app0001.yrapps.cn",
	"pragma": "no-cache",
	"referer": "https://app0001.yrapps.cn/",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "same-origin",
	"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
	"x-requested-with": "XMLHttpRequest",
}
data = {
	"username": "admin",
	"password": "qihuoju10000",
	"vcode": key,
}

init_url = "https://app0001.yrapps.cn/"
init_headers = {
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
	"cache-control": "no-cache",
	"cookie": "PHPSESSID=pllplf8btgv9apvi5ed6geqmqv",
	"pragma": "no-cache",
	"sec-fetch-mode": "navigate",
	"sec-fetch-site": "none",
	"sec-fetch-user": "?1",
	"upgrade-insecure-requests": "1",
	"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}

vcode_url = "https://app0001.yrapps.cn/vcode"
vcode_headers = {
	"accept": "image/webp,image/apng,image/*,*/*;q=0.8",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
	"cache-control": "no-cache",
	"cookie": "PHPSESSID=pllplf8btgv9apvi5ed6geqmqv",
	"pragma": "no-cache",
	"referer": "https://app0001.yrapps.cn/",
	"sec-fetch-mode": "no-cors",
	"sec-fetch-site": "same-origin",
	"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
}

sess = requests.session()
sess.get(init_url,headers=init_headers)
rep = sess.get(vcode_url,headers=vcode_headers)

with open('验证码.png', 'wb') as f:
	f.write(rep.content)
key = input("请输入验证码：")
data['vcode'] = key

rep = sess.post(login_url, data=data, cookies={ "PHPSESSID":"pllplf8btgv9apvi5ed6geqmqv" })

pprint(rep.json())

# sess = requests.session()
# sess.get(init_url,headers=init_headers)
# rep = sess.get(img_url,headers=img_headers)
# with open('验证码.png', 'wb') as f:
# 	f.write(rep.content)

# rep = sess.post(login_url, data=data)
# pprint(rep.json())
# rep = sess.get(index_url, headers=index_headers)
# pprint(rep.text)