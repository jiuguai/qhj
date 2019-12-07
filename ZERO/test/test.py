from urllib import parse
import hashlib
result = parse.unquote("%5Cu96C60%5Cu6781")
print('tracknick',result,u"\u96C60\u6781")

result = parse.unquote("CN%7Czh-CN%7CCNY%7C156")
print('hng',result)

result = parse.unquote("%E9%9B%860%E6%9E%81")
print('lid' ,result)

result = parse.unquote("ccp%3D1")
print(result)

result = parse.unquote("098%23E1hvW9vUvbpvUvCkvvvvvjiPRs5w1jDERLSyQjYHPmPWgjDbP25psj3nRFqvtjEbRphvCvvvvvvCvpvVvvpvvhCvkphvC99vvOCzLTyCvv9vvUvz5lTdAbyCvm9vvvvvphvvvvvv96CvpvQ5vvm2phCvhRvvvUnvphvppvvv96CvpCCvmphvLvAwZvvj8fVxKX6TnVQEfw1lK2kTWlK9D7zwdiB%2Bm7zwaNpqrADn9WmQD404jomxfJClHdUfUzc6AW9XHkx%2F6jc6f4g7EcqOaNoxdXIPvpvhvv2MMTwCvvpvvUmm")
print(result)



md5 = hashlib.md5()

md5.update(b'x')
print(md5.hexdigest())
