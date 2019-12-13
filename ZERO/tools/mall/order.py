import re

from urllib.parse import  urlencode

from pyquery import PyQuery as pq
import pandas as pd
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


    def gen_orders(self,order_type, **kargs):

        doc = pq(self.get_order(order_type, **kargs))

        #   获取列明
        columns = []
        for th in doc('thead th').items():
            columns.append(th.text())
        yield columns

        for tr in doc('tbody tr').items():
            row_l = []
            for v in tr('td').items():
                row_l.append(v.text())
            yield row_l

        item = doc('.pagination>li>a')
        if item.length > 0:
            for page in range(2, int(item[-2].text) + 1):
                kargs.update({"page": page})

                doc = pq(self.get_order(order_type, **kargs))
                for tr in doc('tbody tr').items():
                    row_l = []
                    for v in tr('td').items():
                        row_l.append(v.text())
                    yield row_l



    # 处理商城订单信息

    @staticmethod
    def prc_original_orders(data, **kargs):

        data_info = data['用户信息'].str.extract("""
        (?<=下单人：)(?P<收件人>[^\n]+)
        \s+手机：(?P<联系方式>[^\n]+)
        \s+收货地址：(?P<收货地址>[^\n]+)""", flags=re.S | re.X)


        data_dd = pd.DataFrame(data['订单详情'].apply(extract_detail).to_list())
        return pd.concat([data, data_info, data_dd], axis=1)


    # 护理免费订单信息
    def prc_free_orders(self, data, **kargs):

        data = data.replace("三金美肤面膜 缓解过敏 修复护理|三金美肤面膜 维稳修护 强化屏障", "三金护肤面膜 维稳修护 强化屏障", regex=True)
        patt = '三金补水面膜 镇静维稳 深层补水\\(补水\\)|三金美肤面膜 美白功效 健康肤色\\(美肤\\)|三金护肤面膜 维稳修护 强化屏障\\(护肤\\)|三金水光针\\(水光针\\)'
        data['商品名'] = data['订单详情'].str.extract('(?P<商品名>%s)' % patt, expand=False).str.strip()

        data_info = data['用户信息'].str.extract("""
            (?<=下单人：)(?P<收件人>[^\n]+)
            \s+手机：(?P<联系方式>[^\n]+)
            \s+收货地址：(?P<收货地址>[^\n]+)""", flags=re.S | re.X)
        data = pd.concat([data, data_info], axis=1)
        return data

    def get_pure_orders(self, order_type, order_kargs, **kargs):
        orders = self.gen_orders(order_type, **order_kargs)
        columns = next(orders)
        data_l = []
        for row in orders:
            data_l.append(row)

        data = pd.DataFrame(data_l, columns=columns)

        data['数量'] = data['数量'].astype(int)

        data['下单时间'] = pd.to_datetime(data['下单时间'])
        data['支付时间'] = pd.to_datetime(data['支付时间'])
        # data['redis_pos'] = data['下单时间'].apply(lambda x: x.strftime('%Y:%m:%d'))
        data = data.replace({"支付金额": {"￥": ""}}, regex=True).fillna({"支付金额": 0})
        try:
            data['支付金额'] = data['支付金额'].astype(int)
        except :
            data['支付金额'] = 0
        return data

    def get_free_orders(self, free_goods, order_kargs, **kargs):

        data = self.get_pure_orders('free', order_kargs)

        # patt= "|".join(free_goods['商品名'].unique()).replace("(","\(").replace(")","\)")
        data = self.prc_free_orders(data, **order_kargs)
        if len(data):
            free_data = pd.merge(data
                             , free_goods, on='商品名', how='left')
            return free_data
        return data
    def get_original_orders(self, sku_goods, order_kargs, **kargs):

        data = self.get_pure_orders('original', order_kargs)

        data = self.prc_original_orders(data, **order_kargs)


        if len(data):
            original_data = pd.merge(data, sku_goods[['商品ID', 'goods_type', '单位', '单价']], how='left', on='商品ID')

            return original_data

        return data

    def ext_order(self, order_kargs, sku_goods, free_goods):

        original_data = self.get_original_orders(sku_goods, order_kargs)
        free_data = self.get_free_orders(free_goods, order_kargs)
        data = pd.concat([free_data, original_data], sort=True)
        if len(data):
            l = ['订单号', '订单状态', '商品ID', '下单时间', '支付时间', '支付金额',

                 '商品名', '规格', '单位', '单价', '数量', '备注',

                 '收件人', '联系方式', '收货地址', 'goods_type', '发货商ID', '订单详情']

            data_r = data[l]

            data_r.loc[:, 'name'] = "ORDER:NEW:" + data_r['发货商ID']
            return data_r.reset_index(drop=True)
        return data

def extract_detail(detail):
    gg = []
    for x in re.finditer(".+[\n]|.+$", detail):
        result = re.search("""
                (?P<商品名>.+?)(?=（规格[：:])（
                规格[：:](?P<规格>.+?)(?=[，,]商品ID[：:])
                [，,]商品ID[：:](?P<商品ID>.+)）(?P<数量>\sX\s\d+)""", x[0], re.X)
        d = result.groupdict()
        gg_s = d["规格"] + d['数量']
        gg.append(gg_s)
    d = {
        '商品名': d['商品名'],
        '商品ID': d['商品ID'],
        '规格': "，".join(gg)}
    return d