from hashlib import md5
import datetime
today_s = datetime.datetime.today().strftime("%Y-%m-%d %H")

m = md5(b"jiuguai")

m.update(today_s.encode('utf-8'))
m.update(b'qhj')
m_key = m.hexdigest()[:5]

url = "47.105.186.249?key=%s"
print(url %m_key)