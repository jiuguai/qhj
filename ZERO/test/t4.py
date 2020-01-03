import re
import sys
sys.path.append(r"D:\往期\QHJ\ZERO")
sys.path.append(r"E:\dataparse\Python_DATA_PARSE\QHJ\ZERO")

import warnings
warnings.filterwarnings("ignore")

from tools import *
files_info = {}
files_info['三金'] = r"D:\奇货居\work\外发订单\新订单\三金_新订单 2020-01-03 10_47_40.xlsx"

macro_path = BEAUTY_VBA_PATH
macro_name = "美化.xlsm!bty"
mo = Macro(visible=EXCEL_VISIBLE)
mo.name = macro_name
mo.open(macro_path)

for d_plat,file_path in files_info.items():

    macro_params = (file_path, d_plat,r"新订单|已发未回",)
    mo(params = macro_params)

mo.close()
