import os 
from datetime import datetime

class SaveXl():
    
    def __init__(self, save_dir=None, writer=None,**kargs):


        self.suf = kargs.get('suf'," %s" %(datetime.today().strftime("%Y_%m_%d %H_%M_%S")))
        self.save_dir = save_dir
        self.writer = writer


    def __call__(self, *args, **kargs):
        self.save(*args, **kargs)
    def __setattr__(self, key, value):
        if value is not None and key in {'writer','save_dir'}:
            d = {"writer":None,"save_dir":None}
            d.pop(key)
            self.__dict__.update(d)
        super().__setattr__(key, value)

    def __writer_save(self, data, **kargs):

        data.to_excel(self.writer, sheet_name=self.sheet_name, **kargs) 

    def __excel_save(self, data, **kargs):
        # suf="", pre="", save_dir=""
        self.suf = kargs.pop('suf',self.suf)
        self.pre = kargs.pop('pre',"")
        self.save_dir = kargs.pop('save_dir', self.save_dir)


        file_name = '{pre}{book_name}{suf}.xlsx'.format(book_name=self.book_name,pre=self.pre,suf=self.suf)

        save_path = os.path.join(self.save_dir,file_name)
        data.to_excel(save_path, **kargs) 

        print('已存入 %s' %save_path)


    def save(self, data, name,**kargs):

        self.writer = kargs.get('writer', self.writer)
        kargs.setdefault('index',False)

        if self.writer:
            self.sheet_name = name
            self.__excel_save(data, **kargs)

        else:
            self.book_name = name
            self.__excel_save(data, **kargs)


