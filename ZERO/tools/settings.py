import os

DEBUG = False

# 订单到运单 之间 超时设定
OVERTIME_ORDER_TO_WAYBILL_HOUR = 36


# 工作目录
WORK_DIR = r'D:\奇货居\work'

# 宏文件目录
VBA_DIR = r"D:\奇货居\work\vba"

BEAUTY_VBA_PATH = os.path.join(VBA_DIR, "美化.xlsm")

EXCEL_VISIBLE = 0


# 备份目录
BACK_DIR = r'D:\奇货居\备份'
NEW_ORDER_BAK_DIR = os.path.join(BACK_DIR,r"系统导出\新增订单")
UPDATE_ORDER_BAK_DIR = os.path.join(BACK_DIR,r"系统导出\更新订单")



# 备份供应商 运单目录
TRACKING_BACK_DIR = os.path.join(BACK_DIR,r'运单\源')


# 文件下载目录
EXPORT_DIR = r"D:\Downloads"

# 文件时间格式
DATE_FORMAT = "%Y-%m-%d %H_%M_%S"

"""订单处理
路径 和参数
"""



# 发货商路径

COMMODITY_BASE_DIR = r"D:\奇货居\素材\商城图片素材"
COMMODITY_PATH =os.path.join(COMMODITY_BASE_DIR, "商品信息.xlsx")





# 输出目录
SENDMAIL_ORDER_DIR = os.path.join(WORK_DIR,r"外发订单")

# 订单文件匹配正则
ORDER_DATE_PATT = '^订单(?P<date>20\d{2}(?:-\d{1,2}){2}\D+?\d{1,2}(?:_\d{1,2}){1,2})\.xls[xm]?$'


# 可入系统 目录
INPUT_SYS_DIR = os.path.join(WORK_DIR,r'运单信息\可入系统')

# 可录入系统的 文件匹配正则表达式
INPUT_SYS_PATT = r"运单 (?P<date>\d{4}-\d{1,2}-\d{1,2} \d{1,2}_\d{1,2}_\d{1,2})\.xls[xm]?"


# 运单

TRACKING_SRC_DIR = os.path.join(WORK_DIR,r"运单信息\外部来源")
TRACKING_INPUT_DIR = os.path.join(WORK_DIR,r"运单信息\可入系统")



"""
存储

"""

# 新订单存储目录

NEW_ORDER_SAVE_DIR = os.path.join(WORK_DIR, r"外发订单\新订单")

# 已发订单  未回运单
OVERTIME_ORDER_SAVE_DIR = os.path.join(WORK_DIR, r"外发订单\已发未收")


# 系统字段  映射 本地字段对应关系

FIELDS_SLM_DIC = {

}

# 本地字段 映射 系统字段

FIELDS_LSM_DIC = {v:k for k, v in FIELDS_SLM_DIC.items()}


if DEBUG:
	EXCEL_VISIBLE = 1
