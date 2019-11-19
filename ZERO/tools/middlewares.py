from win32com import client 

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

# 调用宏文件
class MacroMiddleware():
    def __init__(self, macro_path, macro_name, *macro_params, visible=False):
        self.path = macro_path
        self.name = macro_name
        self.params = macro_params

        self.visible = visible

        # self.xlapp = client.Dispatch('Excel.Application')
        # 额外开启进程
        self.xlapp = client.DispatchEx('Excel.Application')

    def run(self):
        try:
            self.xlapp.visible = self.visible
            print('>>>>打开宏表')
            self.book = self.xlapp.Workbooks.Open(self.path)
            print('>>>>开始运行')
            self.xlapp.Application.Run(self.name, *self.params)
            print('>>>>关闭宏表')
            self.xlapp.DisplayAlerts = 0
            self.book.Close()
            
            self.xlapp.Application.Quit()
            print('>>>>关闭完成\n')
        except e:
            print(e)
            pass

        finally:
            self.xlapp.Application.Quit()
        
    def __call__(self):
        self.run()

    def __del__(self):
        self.xlapp.DisplayAlerts = 0
        try:
            self.book.Close()
        except:
            self.xlapp.Application.Quit()
