import sys
import platform
if platform.node() == "zero_PC":
    sys.path.append(r"F:\QHJ\qhj\ZERO")
else:
    sys.path.append(r"D:\往期\QHJ\ZERO")


import numpy as np
import pandas as pd

import pymysql

conn = {
    "user":"root",
    "password":"jiuguai",
    "host":"localhost",
    "port":3306,
    "database":"test",
    "charset" :"utf8mb4"
}
con = pymysql.connect(conn)

cursor = con.cursor()




