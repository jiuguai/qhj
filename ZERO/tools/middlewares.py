from .custom_exception import *
from .tool import get_duplicated_field
import requests
# 输出定单
class OrderOutMiddleware():
    def __init__(self, data, filter_field):
        self.data = data
        self.filter_field = filter_field
        self.sf_dic = {
            "傻傻":self.__ss_out,
        }
        

    # 统一输出 
    def out(self,middleman_name):
        self.temp = self.data[self.data[self.filter_field] == middleman_name]
        func = self.sf_dic.get(middleman_name,self.__default_out)
        return func()

    # 傻傻 输出之前

    def __ss_out(self):
        out_fields = ['订单号','商品ID','商品名','数量','收件人','收货地址','联系方式','备注']
        self.temp.fillna(value={'备注':"", "规格":""}, inplace=True)
        self.temp.loc[:,'备注'] = "规格:" + self.temp['规格'] + "; " + self.temp['备注']
        self.temp.loc[:,'收货地址'] = self.temp['收货地址'] + "[O:" + self.temp['订单号'] + "-" + self.temp['商品ID'] + "]"
        self.temp.replace({"备注":{"规格:; |(规格.+?;) $":r"\1"}},inplace=True,regex=True)

        return self.temp[out_fields]

    def __default_out(self):
        columns = self.temp.columns.tolist()
        print(columns)
        columns.remove("供应商")
        columns.remove("发货商")
        return self.temp[columns]


# 对输入的订单进行处理
class OrderInMiddleware():
    def __init__(self, data):
        self.__data = data
        self.columns = set(data.columns)

    def out(self, **kargs):
        return self.__order_out(**kargs)

    def __call__(self, **kargs):
        return self.out(**kargs)
        


    @property
    def data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data
        self.columns = set(data.columns)


    def __order_out(self, **kargs):
        
        # 更改列名
        re_col = {

        }

        
        data = self.__data.rename(columns=re_col)

        duplicated_fileds = get_duplicated_field(data.columns.tolist())

        if duplicated_fileds:
            raise DFFieldsDupRenamed(",".join(duplicated_fileds))

        columns = set(data.columns)

        # 必须存在的列, 存疑字段：'运单号','用户等级'
        key_fields = {'商品ID', '商品名','规格', '数量', '单位', '收件人', '支付金额', '联系方式', '收货地址', '备注','下单时间' }

        if not key_fields < columns:
            lose_fields = key_fields - columns 
            raise DFFieldsLose(','.join(lose_fields))

        

        return data

