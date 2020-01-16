class Future:
    def __init__(self):
        self.result = 5
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        log('>>callbacks %s' %self._callbacks)
        for fn in self._callbacks:
            fn(self)

    def __iter__(self):
        """
        yield的出现使得__iter__函数变成一个生成器，生成器本身就有next方法，所以不需要额外实现。
        yield from x语句首先调用iter(x)获取一个迭代器（生成器也是迭代器）
        """
        yield self  # 外面使用yield from把f实例本身返回
        return self.result  # 在Task.step中send(result)的时候再次调用这个生成器，但是此时会抛出stopInteration异常，并且把self.result返回

class Crawler:
    def __init__(self,):
 
        self.response = b""

    def fetch(self):
       
        a = yield from Future()
        print("---",a)
        return a




cr = Crawler()
gen = cr.fetch()

x = gen.send(None)
try:
	x = gen.send(None)
except:
	pass


print(x)

