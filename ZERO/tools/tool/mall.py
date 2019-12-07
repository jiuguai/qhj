import requests
from retrying import retry
from ..settings.request_conf import *

# 我们相似但不同  
class MallGoodsInfo():
    """
        original: 商城商品
        free    : 免费领取
    
    """
    def __init__(self, key, **kargs):
        self.key = key


    # 获取当首页信息
    @retry(stop_max_attempt_number=MALL_RETRY_MAX)
    def get_fgoods(self, goods_type="original", **kargs):
        if goods_type == "original":
            url = r'https://app0001.yrapps.cn/admin/Good/goodList'
        else:
            url = r'https://app0001.yrapps.cn/admin/Free/freeList'
        

        headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "cache-control": "no-cache",
                "cookie": "PHPSESSID=%s" %self.key,
                "pragma": "no-cache",
                "referer": "https://app0001.yrapps.cn/admin/Good/goodList",
                "sec-fetch-mode": "nested-navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }
        print('获取首页商品信息')
        rep = requests.get(url,headers=headers,timeout=MALL_GOODS_REQ_TIMEOUT)
        return rep.text

    @retry(stop_max_attempt_number=MALL_RETRY_MAX)
    def get_goods(self, page, goods_type="original", **kargs):
        if goods_type == "original":
            url = r'https://app0001.yrapps.cn/admin/Good/goodList?page=%s'
        else:
            url = r'https://app0001.yrapps.cn/admin/Free/freeList?page=%s'
        headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "cache-control": "no-cache",
                "cookie": "PHPSESSID=%s" %self.key,
                "pragma": "no-cache",
                "referer": "https://app0001.yrapps.cn/admin/Good/goodList",
                "sec-fetch-mode": "nested-navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }

        print('获取第%s页的商品信息' %page)
        rep = requests.get(url %page, headers=headers, timeout=MALL_GOODS_REQ_TIMEOUT)
        return rep.text

    @retry(stop_max_attempt_number=MALL_RETRY_MAX)
    def get_class(self, goods_id, **kargs):
        url = "https://app0001.yrapps.cn/admin/good/good_edit/goods_id/%s.html"

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "cookie": "PHPSESSID=%s" %self.key,
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/Good/goodList?page=1",
            "sec-fetch-mode": "nested-navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }

        print('获取goods_id:%s 的类型' %goods_id)
        rep = requests.get(url %goods_id, headers=headers, timeout=MALL_CLASS_REQ_TIMEOUT)
        
        return rep.text

    @retry(stop_max_attempt_number=MALL_RETRY_MAX)
    def get_attrs(self, goods_id, **kargs):
        url = "https://app0001.yrapps.cn/admin/goodattribute/good_goodattribute"

        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-length": "10",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "PHPSESSID=%s" %self.key,
            "origin": "https://app0001.yrapps.cn",
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/goodattribute/good_attr_conf.html?goods_id=26&a=1.html",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }
        print('获取goods_id:%s 的属性 ' %goods_id)
        rep = requests.post(url, headers=headers, timeout=MALL_ATTR_REQ_TIMEOUT, data={'goods_id':goods_id})
        return rep.json()




class MallGoods(MallGoodsInfo):

    def __init__(self,key,*args,**kargs):

        super().__init__(key)

    @retry(stop_max_attempt_number=MALL_RETRY_MAX)
    def set_attr(self, data):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "content-length": "1350",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "PHPSESSID=%s" % self.key,
            "origin": "https://app0001.yrapps.cn",
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/goodattribute/good_attr_conf.html?goods_id=1&a=1.html",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",

        }
        print('访问 %s' % data['goods_id'])
        url = "https://app0001.yrapps.cn/admin/goodattribute/up_good_attr_conf"
        rep = requests.post(url, headers=headers, data=data, timeout=MALL_ATTR_REQ_TIMEOUT, )
        js = rep.json()
        print(js, data['goods_id'])
        return js
