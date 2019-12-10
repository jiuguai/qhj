import sys
sys.path.append(r"D:\往期\QHJ\ZERO")

from tools import MallGoods,MALL_KEY
mg = MallGoods(MALL_KEY)



goods_path = r"D:\奇货居\素材\商城图片素材\商品信息.xlsx"

df = pd.read_excel(goods_path,index=False,sheet_name="未上传")






goods_id = 26
img_dir = r'D:\ZERO_TEMP\img\test\Huawei Mate 30\轮播'
mg.up_imgs(goods_id,img_dir,"goods_slide")

img_dir = r'D:\ZERO_TEMP\img\test\Huawei Mate 30\详情'
mg.up_imgs(goods_id,img_dir,"goods_info")
