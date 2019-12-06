


class Virtual(Exception):
    pass

# DataFrame 重命名后导致  重名
class DFFieldsDupRenamed(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "重命名后的重复字段: %s" %(self.msg)

# DataFrame 缺失字段
class DFFieldsLose(Exception):
    """
    
    DataFrame 缺失字段
    

    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '%s 字段必须存在' %(self.msg)

class ServiceError(Exception):
    """访问异常
    
    访问服务器异常
    
    Extends:
        Exception
    """

    def __init__(self, msg, obj):
        self.msg = msg
        self.obj = obj

    def __str__(self):
        return self.msg
    