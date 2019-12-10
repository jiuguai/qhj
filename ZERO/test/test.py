import sys
sys.path.append(r"D:\往期\QHJ\ZERO")

import warnings
warnings.filterwarnings('ignore')

from tools import MallGoods,MALL_KEY
mg = MallGoods(MALL_KEY)


import re

print(mg.set_shelf(1,1))