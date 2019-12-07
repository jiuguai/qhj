from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
import time
import os
import re
import json
import random
import requests
from pyquery import PyQuery as pq
import redis

from tools import *
conn = redis.Redis(**DOWNLOAD_TIANMAO_PIC_DIC)


urls = {
    "Huawei Mate 30":"https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.7.46b210b2EOc9Nq&id=606306790423&skuId=4245743516766&areaId=430100&standard=1&user_id=2838892713&cat_id=2&is_b=1&rn=ac86a186cc50b8320a818218584e7d6c",
    "Huawei Mate 30 Pro":"https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.46b210b2EOc9Nq&id=606307762219&skuId=4419631387556&areaId=430100&standard=1&user_id=2838892713&cat_id=2&is_b=1&rn=ac86a186cc50b8320a818218584e7d6c",
    "iPhone 11":"https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.963c368enRWX8p&id=602659642364&skuId=4387862094596&areaId=430100&standard=1&user_id=1917047079&cat_id=2&is_b=1&rn=8f138c928b23064189b241a24c6537e1",
    "iPhone 11 Pro":"https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.29.963c368enRWX8p&id=602451153900&skuId=4387862322527&areaId=430100&standard=1&user_id=1917047079&cat_id=2&is_b=1&rn=8f138c928b23064189b241a24c6537e1",
    "iPhone 11 Pro Max":"https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.7.963c368enRWX8p&id=602451665186&skuId=4387862510070&areaId=430100&standard=1&user_id=1917047079&cat_id=2&is_b=1&rn=8f138c928b23064189b241a24c6537e1",
    "七匹狼":"https://detail.tmall.com/item.htm?spm=a1z10.1-b-s.w5003-22181859704.6.9f9b3a16WyVyen&id=577025909674&scene=taobao_shop&skuId=3973098010411",
}
headers = {
"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
"cache-control": "no-cache",
"cookie":"cna=b5dJFlMvl2ECAa8IsxkB2wYK; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E9%9B%860%E6%9E%81; enc=JsZ6y6r9t7pJ5xObUYpd24FXEPfc0H0VJJZLGAMKt8sZwtdigEbkDmbxMmheDy6e6xJAyUGNSneYZ5UkROdYUw%3D%3D; cq=ccp%3D1; t=da009be74fe7e8987a56b4c863331289; uc3=nk2=3zY0LDQ%3D&vt3=F8dByua%2FI62GrJlsTEQ%3D&id2=UUkGVJHeIputLA%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=%5Cu96C60%5Cu6781; uc4=nk4=0%403cIrCkqmW75J0Z2KYRo7Bg%3D%3D&id4=0%40U2uKc%2BNfWQRDgT3ckBpEht46%2FNFf; lgc=%5Cu96C60%5Cu6781; _tb_token_=e4e30e9f53e1e; cookie2=1e8c1015c8f07536ebc3fc596d2ba3d2; _m_h5_tk=38589e59bb4da943c32b6229ce3c5326_1575724338819; _m_h5_tk_enc=7128e5f1aeb3e53f2d1285d872ba5df0; pnm_cku822=098%23E1hvXpvUvbpvUpCkvvvvvjiPRs5wAj3bP2dUAjEUPmPvsjEVRFdZgjlnRFLwgjnmRTwCvvpvvUmmvphvC9v9vvCvpbyCvm9vvv2UphvvEpvvvzrvpvLQvvm2phCvhRvvvUnvphvppvvv9QnvpCvCkphvC99vvOCzLTyCvv9vvUvzIW6AzQyCvhQUqGWvCsfWaNmxdX3tEbk1DfesRk9czWLvgC0wJhjU%2BneYr2E9ZRAn3w0AhjHUTWex6fItb9TxfwCl533%2BCNLy0nQXHFXXiXVvQE012QhvCvvvvvvtvpvhvvvvvv%3D%3D; l=dBT7zjKlqZXIskxbBOCg5uI8aPbOSIRAguPRwNcXi_5BE6L_59_OkhVNSFp6VjWft8YB4HAa5Iy9-etumJpTY-fP97Rw_xDc.; isg=BOXl0rrw1A_ysDD6_gi_0zSB9KHfipnRcfMruefKoZwr_gVwr3KphHMciCItfrFs",
"pragma": "no-cache",
"referer": "http://list.tmall.com/search_product.htm?q=%BB%AA%CE%AA%CA%D6%BB%FA&type=p&vmarket=&spm=a2233.7711963.a2227oh.d100&from=..pc_1_searchbutton",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "same-origin",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}

cookies = [
    "cna=b5dJFlMvl2ECAa8IsxkB2wYK; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E9%9B%860%E6%9E%81; enc=JsZ6y6r9t7pJ5xObUYpd24FXEPfc0H0VJJZLGAMKt8sZwtdigEbkDmbxMmheDy6e6xJAyUGNSneYZ5UkROdYUw%3D%3D; cq=ccp%3D1; t=da009be74fe7e8987a56b4c863331289; uc3=nk2=3zY0LDQ%3D&vt3=F8dByua%2FI62GrJlsTEQ%3D&id2=UUkGVJHeIputLA%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=%5Cu96C60%5Cu6781; uc4=nk4=0%403cIrCkqmW75J0Z2KYRo7Bg%3D%3D&id4=0%40U2uKc%2BNfWQRDgT3ckBpEht46%2FNFf; lgc=%5Cu96C60%5Cu6781; _tb_token_=e4e30e9f53e1e; cookie2=1e8c1015c8f07536ebc3fc596d2ba3d2; _m_h5_tk=38589e59bb4da943c32b6229ce3c5326_1575724338819; _m_h5_tk_enc=7128e5f1aeb3e53f2d1285d872ba5df0; pnm_cku822=098%23E1hvy9vUvbpvU9CkvvvvvjiPRs5wAj3bnLLptjljPmPv1jiWRFLwgj18R2sUsjr2PF%2BtvpvhvvvvvvGCvvLMMQvvkphvC99vvOCzLTyCvv9vvUvzIWqcFfyCvm9vvv2UphvvEpvvvzrvpvLQvvm2phCvhRvvvUnvphvppvvv9QnvpCvCmphvLvkPFQvjcWCl%2BE7rVC69kUkQD464jomnfaBlHdUfbcc60f06WeCp%2BExrt8TJwHADYWLWVB3QcneYiXhpVj%2BO3w0x9CyOJ9kx6acEn1vCvpvVvmvvvhCviQhvCvvv9UU%3D; l=dBT7zjKlqZXIsKRbBOCg5uI8aPbOSIRAguPRwNcXi_5pq6L_-0bOkhVZiFp6VjWft8YB4HAa5Iy9-etux-pTY-fP97Rw_xDc.; isg=BKenjmQ-tlVkvjLwwDYd-eK3NtuxhHtrRyWpM3kUwzZdaMcqgfwLXuXiiijTgFOG",
    "cna=b5dJFlMvl2ECAa8IsxkB2wYK; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E9%9B%860%E6%9E%81; enc=JsZ6y6r9t7pJ5xObUYpd24FXEPfc0H0VJJZLGAMKt8sZwtdigEbkDmbxMmheDy6e6xJAyUGNSneYZ5UkROdYUw%3D%3D; cq=ccp%3D1; t=da009be74fe7e8987a56b4c863331289; uc3=nk2=3zY0LDQ%3D&vt3=F8dByua%2FI62GrJlsTEQ%3D&id2=UUkGVJHeIputLA%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=%5Cu96C60%5Cu6781; uc4=nk4=0%403cIrCkqmW75J0Z2KYRo7Bg%3D%3D&id4=0%40U2uKc%2BNfWQRDgT3ckBpEht46%2FNFf; lgc=%5Cu96C60%5Cu6781; _tb_token_=e4e30e9f53e1e; cookie2=1e8c1015c8f07536ebc3fc596d2ba3d2; _m_h5_tk=38589e59bb4da943c32b6229ce3c5326_1575724338819; _m_h5_tk_enc=7128e5f1aeb3e53f2d1285d872ba5df0; pnm_cku822=098%23E1hvXpvUvbpvUpCkvvvvvjiPRs5wAj3bP2dUAjEUPmPvsjEVRFdZgjlnRFLwgjnmRTwCvvpvvUmmvphvC9v9vvCvpbyCvm9vvv2UphvvEpvvvzrvpvLQvvm2phCvhRvvvUnvphvppvvv9QnvpCvCkphvC99vvOCzLTyCvv9vvUvzIW6AzQyCvhQUqGWvCsfWaNmxdX3tEbk1DfesRk9czWLvgC0wJhjU%2BneYr2E9ZRAn3w0AhjHUTWex6fItb9TxfwCl533%2BCNLy0nQXHFXXiXVvQE012QhvCvvvvvvtvpvhvvvvvv%3D%3D; l=dBT7zjKlqZXIskxbBOCg5uI8aPbOSIRAguPRwNcXi_5BE6L_59_OkhVNSFp6VjWft8YB4HAa5Iy9-etumJpTY-fP97Rw_xDc.; isg=BOXl0rrw1A_ysDD6_gi_0zSB9KHfipnRcfMruefKoZwr_gVwr3KphHMciCItfrFs",
    "cna=b5dJFlMvl2ECAa8IsxkB2wYK; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E9%9B%860%E6%9E%81; enc=JsZ6y6r9t7pJ5xObUYpd24FXEPfc0H0VJJZLGAMKt8sZwtdigEbkDmbxMmheDy6e6xJAyUGNSneYZ5UkROdYUw%3D%3D; cq=ccp%3D1; t=da009be74fe7e8987a56b4c863331289; uc3=nk2=3zY0LDQ%3D&vt3=F8dByua%2FI62GrJlsTEQ%3D&id2=UUkGVJHeIputLA%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=%5Cu96C60%5Cu6781; uc4=nk4=0%403cIrCkqmW75J0Z2KYRo7Bg%3D%3D&id4=0%40U2uKc%2BNfWQRDgT3ckBpEht46%2FNFf; lgc=%5Cu96C60%5Cu6781; _tb_token_=e4e30e9f53e1e; cookie2=1e8c1015c8f07536ebc3fc596d2ba3d2; _m_h5_tk=38589e59bb4da943c32b6229ce3c5326_1575724338819; _m_h5_tk_enc=7128e5f1aeb3e53f2d1285d872ba5df0; pnm_cku822=098%23E1hvfQvUvbpvUvCkvvvvvjiPRs5wAj3Wn2zyljivPmPZAjYRPsqy0jrmRL5hAjEHmphvLvhJW2vaiC4AdX31bPLWeX7AdcOd%2BE7rVTTJEcqyaBRAdX31bbmxdX9OdegJlw66Hb8rakKy%2Bb8rVTtYVVzhV8g7%2B3%2BSaNoAdBKKfvetvpvIvvCv6pvvv8pvvh4Qvvmvj9vvBGwvvvUwvvCj1Qvvv99vvhaCvvvmU8yCvv9vvhhS9GVanIyCvvOCvhE2zRvCvpvVvvBvpvvv2QhvCvvvMMGtvpvhvvCvp8wCvvpvvhHh; l=dBT7zjKlqZXIsQb9BOCg5uI8aPbOSIRAguPRwNcXi_5dq6YsmKQOkhVavFv6VjWft8YB4HAa5Iy9-etumJpTY-fP97Rw_xDc.; isg=BKys_0dF3ZSjGMmBH6_GWAUufYoezVBqwCwyYgbtuNf6EUwbLnUgn6IjMZkMmYhn",
    "cna=b5dJFlMvl2ECAa8IsxkB2wYK; hng=CN%7Czh-CN%7CCNY%7C156; lid=%E9%9B%860%E6%9E%81; enc=JsZ6y6r9t7pJ5xObUYpd24FXEPfc0H0VJJZLGAMKt8sZwtdigEbkDmbxMmheDy6e6xJAyUGNSneYZ5UkROdYUw%3D%3D; cq=ccp%3D1; t=da009be74fe7e8987a56b4c863331289; uc3=nk2=3zY0LDQ%3D&vt3=F8dByua%2FI62GrJlsTEQ%3D&id2=UUkGVJHeIputLA%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D; tracknick=%5Cu96C60%5Cu6781; uc4=nk4=0%403cIrCkqmW75J0Z2KYRo7Bg%3D%3D&id4=0%40U2uKc%2BNfWQRDgT3ckBpEht46%2FNFf; lgc=%5Cu96C60%5Cu6781; _tb_token_=e4e30e9f53e1e; cookie2=1e8c1015c8f07536ebc3fc596d2ba3d2; _m_h5_tk=38589e59bb4da943c32b6229ce3c5326_1575724338819; _m_h5_tk_enc=7128e5f1aeb3e53f2d1285d872ba5df0; pnm_cku822=098%23E1hvTpvUvbpvUvCkvvvvvjiPRs5wAj3nPscO1jYHPmP90jEmP2d9ljnVPFS9tjDWiQhvCvvv9UUEvpCWmhqevvwzaNoxfBy4jLPEDaexRfyD24oQD76XVB69D7zUQ8gc8y7DK4mUhXB%2Bm7zhgj7J%2B3%2BiAj7QiXT4JhSU%2BneYr2E9ZRAn3w0AhbyCvm9vvv2UphvvEpvvvzrvpvLQvvm2phCvhRvvvUnvphvppvvv9QnvpCvCkphvC99vvOCzLTyCvv9vvUvzInHQ99hCvvOvUvvvphvPvpvhvv2MMsyCvvpvvvvv; l=dBT7zjKlqZXIsMGyBOCg5uI8aPbOSIRAguPRwNcXi_5IL6L_FUQOkhV13Fp6VjWft8YB4HAa5Iy9-etumJpTY-fP97Rw_xDc.; isg=BGZmz52cBxoO5NOXKQ0s5jtst9wo76pk7q6I1FAPUglk0wbtuNf6EUwhK496-6IZ",
]


def save_img(file_name ,url):

    rep = requests.get(url)
    print(url ,"\n",file_name)
    with open(file_name, 'wb') as f:
        f.write(rep.content)


save_dir = r"D:\ZERO_TEMP\img\test"

# 用于下载图片



# conn.delete('tm_imgs')
# for goods_name, url in urls.items():
#     headers['cookie'] = random.choice(cookies)
#     d = {}
#     d['images'] = {}
#     d['images']['head'] = []
#     d['images']['desc'] = []
#
#     goods_dir = os.path.join(save_dir,goods_name)
#
#     desc_dir = os.path.join(goods_dir,'详情')
#     slide_dir = os.path.join(goods_dir,'轮播')
#     os.makedirs(desc_dir,exist_ok=True)
#     os.makedirs(slide_dir,exist_ok=True)
#
#     print('请求 %s %s' %(goods_name, url))
#     rep = requests.get(url,headers=headers)
#
#     html = rep.text
#     d['content'] = html
#
#     doc = pq(html)
#     lis = doc(".tb-img li")
#     item_info_s = re.search('(?<=TShop.Setup\().+?(?=\);)', html,re.S|re.M).group()
#     item_info = json.loads(item_info_s)
#
#
#     for li in lis:
#         color_name = li.attrib['title']
#         data_value = ";" + li.attrib['data-value']+";"
#         try:
#             img_url = "http:" + item_info["propertyPics"][data_value][0]
#         except:
#             img_url = "http:" + re.search('(?<=skuMap).+?'+ data_value +'.+?images.+?(//.+?)(?=")',item_info_s,re.M).group(1)
#
#         save_path = os.path.join(slide_dir,color_name+".jpg")
#         d['images']['head'].append({
#             "save_path":save_path,
#             'url':img_url
#         })
#
#
#
#     desc_url = "https:" + item_info['api']['descUrl']
#
#     print('请求详情 %s %s' % (goods_name, url))
#     # 获取详情
#     desc_rep = requests.get(desc_url,headers = headers)
#
#     desc_html = desc_rep.text
#     desc_doc = pq(desc_html[10:-3])
#
#     for i,img in enumerate(desc_doc('img')):
#         img_url = img.attrib['src']
#         save_path = os.path.join(desc_dir,'%s.jpg' %i)
#         d['images']['desc'].append({
#             "save_path": save_path,
#             'url': img_url
#         })
#     conn.lpush('tm_imgs',json.dumps(d))






#     d = {}
#     d['images'] = {}
#     d['images']['head'] = []
#     d['images']['desc'] = []


excecutor = ThreadPoolExecutor(max_workers=10)

while conn.llen('tm_imgs'):
    img_info = conn.rpop("tm_imgs")
    conn.lpush('tm_imgs_r',img_info)
    img_info = json.loads(img_info)
    for down_info in img_info['images']['head']:
        save_path = down_info['save_path']
        img_url = down_info['url']
        excecutor.submit(save_img,save_path, img_url)

    for down_info in img_info['images']['desc']:
        save_path = down_info['save_path']
        img_url = down_info['url']
        excecutor.submit(save_img,save_path, img_url)
excecutor.shutdown(True)
print('下载完毕')