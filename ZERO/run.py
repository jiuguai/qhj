import sys
# import app
import importlib

select_map = {
	'describe':'[2] 运单信息',
	'func':None,
	1:{
		'describe':'[1] 订单信息',
		'func':None,
		1:{
			"func":"app.order_sys2local_process.run",
			"describe":"[1] 商城订单信息提取"
		},
		2:{
			"func":"app.order_insert_mysql.run",
			"describe":"[2] 同步本地"
		},
	},
	2:{
		'describe':'[2] 运单信息',
		'func':None,
		1:{
			"func":"app.waybill_update_mall.run",
			"describe":"[1] 商城运单信息更新"
		},
		2:{
			"func":"app.waybill_update_mysql.run",
			"describe":"[2] 同步本地"
		},
	},
	
	3:{
		"func":"app.order_trace.run",
		"describe":"[3] 生成订单跟踪信息"
	}
}

l = [select_map]

while True:

	handle_map = l[-1]

	for i in range(1, len(handle_map)-1):
		print(handle_map[i]['describe'])

	if len(l) == 0:
		print('[q] 退出')
	else:
		print('[0] 返回上级')
		print('[q] 退出')

	a = input('请输入>>>>')
	if a.isnumeric():
		a = int(a)

		if a == 0:
			if len(l) > 1:
				l.pop()
			continue
		
		imp_name = handle_map[a]['func']

		if imp_name is None:
			l.append(handle_map[a])
			continue

		module_name, func_name = imp_name.rsplit('.',1)

		module = importlib.import_module(module_name)
		func = getattr(module, func_name)
		func()

	elif a == 'q':
		break


