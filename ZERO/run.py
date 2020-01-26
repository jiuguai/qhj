import sys
# import app
import importlib

select_map = {
	1:{
		"func":"app.order_sys2local_process.run",
		"describe":"[1] 提取订单信息"
	},
	2:{
		"func":"app.order_insert_mysql.run",
		"describe":"[2] 将订单信息备份到本地数据"
	},
	3:{
		"func":"app.waybill_update_mall.run",
		"describe":"[3] 更新运单信息到系统"
	},
	4:{
		"func":"app.waybill_update_mysql.run",
		"describe":"[4] 更新运单信息到本地"
	},
	5:{
		"func":"app.order_trace.run",
		"describe":"[5] 生成订单跟踪信息"
	}
}

while True:
	for i in range(1, len(select_map)+1):
		print(select_map[i]['describe'])
	print('[0] 退出')
	a = input('请输入>>>>')
	if a.isnumeric():
		a = int(a)
		if a == 0:
			break
		imp_name = select_map[a]['func']
		module_name, func_name = imp_name.rsplit('.',1)

		module = importlib.import_module(module_name)
		func = getattr(module, func_name)
		func()


