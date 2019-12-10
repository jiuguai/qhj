import random
import os
import datetime
import hashlib
import re
import requests


from retrying import retry
from pyquery import PyQuery as pq
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
            # "content-length": "10",
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

    @retry(stop_max_attempt_number=2)
    def set_shelf(self, goods_id, is_shelf):
        url = "https://app0001.yrapps.cn/admin/good/good_opt_shelf.html"
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            # "content-length": "21",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "PHPSESSID=%s" %self.key,
            "origin": "https://app0001.yrapps.cn",
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/Good/goodList",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        data = {
            "goods_id": goods_id,
            "is_shelf": is_shelf
        }
        state = "上架" if is_shelf else "下架"
        print('goods_id:%s 设为%s' %(goods_id, state))
        rep = requests.post(url, headers=headers, data=data)
        return rep.json()

class MallGoodsAttrs():
    def __init__(self, key, **kargs):
        self.key = key

    def _format_decimal(self, num):
        try:
            num = num if num % int(num) else int(num)
        except ZeroDivisionError:
            num = 0
        return num

    def _make_attr(self, index, row):
        attr_name_list = row['attr_name'].split('|')

        attr_d = {

            "attr_list[%s][attr_name]" % (index): " ".join(attr_name_list),
            "attr_list[%s][attr_price]" % (index): self._format_decimal(row["attr_price"]),
            "attr_list[%s][attr_stock]" % (index): int(row["attr_stock"]),

            "attr_list[%s][attr_goods_code]" % (index): row["attr_goods_code"],
            "attr_list[%s][goods_id]" % (index): row["goods_id"],
            "attr_list[%s][attr_unit]" % (index): row["attr_unit"],
            "attr_list[%s][attr_old_price]" % (index): self._format_decimal(row["attr_old_price"]),

        }

        for attr_name_i, attr_name in enumerate(attr_name_list):
            attr_d["attr_list[%s][attr_name_list][%s][attr_name]" % (index, attr_name_i)] = attr_name

        return attr_d

    def gen_attr(self, df, goods_id):
        data = {"goods_id": goods_id}
        for index, row in df.reset_index(drop=True).iterrows():
            data.update(self._make_attr(index, row))
        return data

    def _gen_attrs(self, goods_df):
        gdb = goods_df.groupby('goods_id')
        for goods_id, df in gdb:
            yield self.gen_attr(df, goods_id)


    # 批量修改
    def set_attrs(self,df):
        for data in self._gen_attrs(df):
            self.set_attr(data)

    # 耽搁修改
    @retry(stop_max_attempt_number=MALL_RETRY_MAX)
    def set_attr(self, data):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            # "content-length": "1350",
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


class MallImages():

    random_chart = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'
    com = re.compile(r'^\d+(?=[\._].*?(?:jpg|png)$)')

    def __init__(self, key, **kargs):
        self.key = key
    @retry(stop_max_attempt_number=2)
    def up_shop_img(self, goods_id, file_path):
        with open(file_path, 'rb') as f:
            content = f.read()

        files = {

            'file': ('%s.jpg' % ("".join(random.sample(self.random_chart, k=12))), content, "image/jpeg"),

        }
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            # "content-length": "395314",
            # "content-type": "multipart/form-data; boundary=--89369e8a552b416eb56f7efcc2cf5f28",

            "cookie": "PHPSESSID=%s" % self.key,
            "origin": "https://app0001.yrapps.cn",
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/Good/goodList?page=1",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",

        }
        md5 = hashlib.md5()  # b'shop_img'
        md5.update(content)
        data = {
            'goods_id': goods_id,
            'goods_img': r"/uploads/%s/%s.jpg" % (datetime.date.today().strftime('%Y%m%d'), md5.hexdigest())
        }
        url = "https://app0001.yrapps.cn/admin/good/update_shop_img.html"
        print('updload %s' % file_path)
        rep = requests.post(url, headers=headers, data=data, files=files, timeout=5)
        js = rep.json()
        print('%s %s' % (js, file_path))
        return js

    @retry(stop_max_attempt_number=2)
    def get_imgs(self, goods_id, img_class):
        if img_class == "goods_slide":
            url = 'https://app0001.yrapps.cn/admin/slide/slideList/type_id/%s/img_class/goods_slide.html' % goods_id
            msg = "获取 %s slide IMG"
        elif img_class == "goods_info":
            url = 'https://app0001.yrapps.cn/admin/slide/slideList/type_id/%s/img_class/goods_info.html' % goods_id
            msg = "获取 %s 详情 IMG"
        headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            "cookie": "PHPSESSID=%s" % self.key,
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/Good/goodList",
            "sec-fetch-mode": "nested-navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",

        }
        print(msg % goods_id)
        rep = requests.get(url, headers=headers)
        doc = pq(rep.text)
        imgs = doc('[img_id]')

        slide_imgs = []
        for img in imgs.items():
            img_id = img.attr('img_id')
            img_url = img.attr('src')
            data = {
                "img_id": img_id,
                "img_url": img_url
            }
            slide_imgs.append(data)
        return slide_imgs

    @retry(stop_max_attempt_number=2)
    def del_imgbox(self, img_info, goods_id):
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            # "content-length": "19",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "PHPSESSID=%s" % self.key,
            "origin": "https://app0001.yrapps.cn",
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/slide/slideList/type_id/%s/img_class/goods_slide.html" % goods_id,
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        url = "https://app0001.yrapps.cn/admin/slide/del_slide.html"
        print('删除imgbox %s' % img_info['img_id'])
        rep = requests.post(url, headers=headers, data=img_info)

        return rep.json()

    @retry(stop_max_attempt_number=2)
    def add_imgbox(self, goods_id, img_class):
        """

        :param goods_id:    商品ID
        :param img_class:   "goods_info": "给goods_id:%s添加详情box",
                            "goods_slide": "给goods_id:%s添加轮播box"
        :return:  返回操作结果
        """

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            # "content-length": "19",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "PHPSESSID=%s" % self.key,
            "origin": "https://app0001.yrapps.cn",
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/slide/slideList/type_id/%s/img_class/goods_slide.html" % goods_id,
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        ret_inof = {
            "goods_info": "给goods_id:%s添加详情box",
            "goods_slide": "给goods_id:%s添加轮播box"
        }

        data = {
            "img_class": img_class,
            "type_id": goods_id
        }
        url = "https://app0001.yrapps.cn/admin/slide/add_slide.html"
        # print(ret_inof[img_class] %goods_id)
        rep = requests.post(url, headers=headers, data=data)

        return rep.json()

    @retry(stop_max_attempt_number=2)
    def up_img(self, img_info, file_path, img_class, goods_id):
        """

            :param goods_id:    商品ID
            :param img_class:   "goods_info": "给goods_id:%s添加详情box",
                                "goods_slide": "给goods_id:%s添加轮播box"
            :return:  返回操作结果
        """
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "no-cache",
            # "content-length": "64574",
            # "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryamFD6p55BM3okoE1",
            "cookie": "PHPSESSID=%s" % self.key,
            "origin": "https://app0001.yrapps.cn",
            "pragma": "no-cache",
            "referer": "https://app0001.yrapps.cn/admin/slide/slideList/type_id/%s/img_class/goods_slide.html" % goods_id,
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }

        url = "https://app0001.yrapps.cn/admin/slide/img_slide.html"

        with open(file_path, 'rb') as f:
            content = f.read()

        md5 = hashlib.md5()
        md5.update(content)
        data = {
            "img_class": img_class,
            "img_id": img_info['img_id'],
            "img_url": "/uploads/%s/%s.jpg" % (datetime.date.today().strftime("%Y%m%d"), md5.hexdigest()),
        }
        files = {
            'file': (os.path.split(file_path)[1], content, "image/jpeg")
        }

        print('上传 %s' % file_path)
        rep = requests.post(url, headers=headers, data=data, files=files)
        return rep.json()

    def _sort_files(self, files):
        l = []
        for file_name in files:
            index = self.com.match(file_name)
            if index:
                l.append((
                    int(index.group()),
                    file_name
                ))
        l.sort(key=lambda x: x[0])
        return l

    def up_imgs(self, goods_id, img_dir, img_class):

        # 删除所有 slide
        for img_info in self.get_imgs(goods_id, img_class):
            self.del_imgbox(img_info, goods_id)

        # 创建 slide

        files = self._sort_files(os.listdir(img_dir))
        for i, img in files:
            print('给%s 添加个box' % img)

            self.add_imgbox(goods_id, img_class)

        # 上传图片
        first_slide_path = None

        print('上传')
        for (file_index, file_name), img_info in zip(files, self.get_imgs(goods_id, img_class)):

            file_path = os.path.join(img_dir, file_name)

            if first_slide_path is None and img_class=="goods_slide":
                first_slide_path = file_path

            print(img_info, file_path, img_class, goods_id)
            self.up_img(img_info, file_path, img_class, goods_id)


        if first_slide_path is not None:
            self.up_shop_img(goods_id, first_slide_path)


        print('上传完毕')


class MallGoods(MallGoodsInfo, MallGoodsAttrs, MallImages):

    def __init__(self,key,*args,**kargs):
        self.key = key
        # super().__init__(key)

