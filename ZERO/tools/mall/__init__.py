from .goods import *
from .order import *

class Mall(MallGoods,MallOrder):
    def __init__(self, key):
        self.key = key

QHJMall = Mall