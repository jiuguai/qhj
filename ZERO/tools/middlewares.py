

# 输出定单
class OutOrderMiddleware():
    def __init__(self, data, filter_field):
        self.data = data
        self.filter_field = filter_field
        self.sf_dic = {
            "傻傻":self._ss_out,
        }
        

    # 统一输出
    def out(self,middleman_name):
        self.temp = self.data[self.data[self.filter_field] == middleman_name]
        func = self.sf_dic.get(middleman_name,self._default_out)
        return func()

    # 傻傻 输出之前

    def _ss_out(self):
        out_fields = ['商品名','数量','收件人姓名','收件人地址','收件人电话','备注']

        self.temp.loc[:,'备注'] = "规格:" + self.temp['规格'] + "; " + self.temp['备注']
        self.temp.loc[:,'收件人地址'] = self.temp['收件人地址'] + "[W:" + self.temp['订单号'] + "]"
        return self.temp[out_fields]

    def _default_out(self):
        return self.temp

