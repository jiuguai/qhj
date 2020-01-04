import re
patt = "^(?P<company>[^_]+?)(?=运单_)"
# patt = "(?<=^趣领_)(?P<company>[^_]+)"
file_name = "三金运单_2020年1月4日09:37:35.xlsx"
com = re.compile(patt)
r = com.search( file_name)
if r:
	print(r.groupdict()['company'])