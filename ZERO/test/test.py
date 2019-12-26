1. 读取
	1. 我要从系统中获取订单数据	a
	2. 读取本地商品信息表  		b
2. 处理
	1. 将a 的字段统一字段名
	2. 将a 数据按照 `订单号` 去重
	3. 将一单多商品 进行 进行拆分 以订单号和商品ID 组合为为唯一健
	4. 将a 和 b 关于商品ID进行关联
	5. 按照不同生产 厂商进行分类 生成不同厂商需要的文件
3. 分发供应商
	
4. 收到运单信息
	1. 检查数据
	2. 进行上传


# 存不存在一种
# 
# 
# 统一字段
rename_cols = {
	"f1":"a1",
	"f2":"a1",
}
df.rename(columns={rename_cols})


"""字段检测

必须要的字段
"""
expect_cols = {"a1","a2"}

if not expect_col - set(df):
	print('先检查字段是否齐全或者字段名是否准确')
	sys.exit()


"""
# 统一类型
# index_type

"""
col_types = {
	
	"a1":int,
	"a2":"int",
	"a3":str
}
# 很重要
# 过程中报错 必须检查 不可忽略 
for col, col_type in col_types.items():
	df[col] = df[col].astype(col_type)


"""


"""









