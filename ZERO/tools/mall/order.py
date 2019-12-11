from urllib.parse import  urlencode

from retrying import retry
import requests


class MallOrder():
    def __init__(self, key ):
        self.key = key


    @retry(stop_max_attempt_number=2)
    def get_order(self, order_type, **kargs):
        """
        params = {
            # 请求类型 0 表示所有订单 1 未发货  2 已发货
            # 3 已完成 4 申请退款 5 退款成功  10 未支付
            "order_status": kargs.get("order_status", 0),
            "order_time": kargs.get("order_time", ""), # today yesterday week month
            "order_id": kargs.get("order_id", ""), # 订单号
            "order_type": order_type,  # original free
            "page": kargs.get("page", 1),  #
        }
        """
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "cookie": "PHPSESSID=%s" %self.key,
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/index/index",
            "sec-fetch-mode": "nested-navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }
        url = "https://app0001.yrapps.cn/admin/Order/orderList"
        params = {
            "order_status": kargs.get("order_status", 0),
            "order_time": kargs.get("order_time", ""),
            "order_id": kargs.get("order_id", ""),
            "order_type": order_type,
            "page": kargs.get("page", 1),
        }
        print('请求 %s' %params)
        rep = requests.get(url + "?" + urlencode(params), headers=headers)

        return rep.text


