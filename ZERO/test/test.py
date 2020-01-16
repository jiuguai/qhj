import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
stopped = False
urls_todo = {"/", "/1", "/2", "/3"}
urls_todo = {"/"}
def log(info):
    print(">>>> %s" %info)
class Future:
    def __init__(self):
        self.result = None
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

def connect(sock, address):
    f = Future()
    log('in connected')
    sock.setblocking(False)
    try:
        sock.connect(address)
    except BlockingIOError:
        pass

    def on_connected():
        
        f.set_result(None)

    selector.register(sock.fileno(), EVENT_WRITE, on_connected)
    log('1 connect')
    yield from f
    log('2 connect')
    selector.unregister(sock.fileno())

def read(sock):
    f = Future()

    def on_readable():
        log('on_readable')
        f.set_result(sock.recv(100))
    log(sock.fileno())
    selector.register(sock.fileno(), EVENT_READ, on_readable)
    """
    此处的chunck接收的是f中return的f.result，同时会跑出一个stopIteration的异常，只不过被yield from处理了。
    这里也可直接写成chunck = yiled f
    """
    log('1 read')
    chunck = yield from f
    log('2 read')
    selector.unregister(sock.fileno())
    return chunck

def read_all(sock):
    response = []
    chunk = yield from read(sock)
    log(chunk)
    while chunk:
        response.append(chunk)
        chunk = yield from read(sock)
        log(chunk)
    return b"".join(response)

class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b""
        log('初始化 Crawler')
    def fetch(self):
        
        global stopped
        log('1 fetch')
        sock = socket.socket()
        yield from connect(sock, ("xkcd.com", 80))
        log('2 fetch')
        get = "GET {0} HTTP/1.0\r\nHost:xkcd.com\r\n\r\n".format(self.url)
        sock.send(get.encode('ascii'))
        self.response = yield from read_all(sock)
        print(self.response)
        urls_todo.remove(self.url)
        if not urls_todo:
            stopped = True

class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)  # 激活Task包裹的生成器
        log('first connect %s' %f._callbacks)

    def step(self, future):
        log('step')
        try:
            # next_future = self.coro.send(future.result)
            next_future = self.coro.send(None)  # 驱动future
        except StopIteration:
            log('end')
            return

        next_future.add_done_callback(self.step)

def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            log('--'*30)
            log('loop')

            callback()

if __name__ == "__main__":
    import time
    start = time.time()
    for url in urls_todo:
        crawler = Crawler(url)
        Task(crawler.fetch())
    print('start')
    loop()
    print(time.time() - start)