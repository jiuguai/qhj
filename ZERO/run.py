import sys
import platform
if platform.node() == "zero_PC":
    sys.path.append(r"F:\QHJ\qhj\ZERO")
else:
    sys.path.append(r"D:\往期\QHJ\ZERO")

import warnings
warnings.filterwarnings('ignore')

# import app
import importlib

select_map = {
    'describe': '奇货居事务处理',
    'func': None,
    1: {
        'describe': '[%s] 订单',
        'func': None,
        1: {
            "func": "app.order_sys2local_process.run",
            "describe": "[%s] 商城订单信息提取"
        },
        2: {
                    "func": "app.order_insert_mysql.run",
                    "describe": "[%s] 同步本地"
                },
    },
    2: {
        'describe': '[%s] 运单',
        'func': None,
        1: {
            "func": "app.waybill_update_mall.run",
            "describe": "[%s] 商城运单信息更新"
        },
        2: {
            "func": "app.waybill_update_mysql.run",
            "describe": "[%s] 同步本地"
        },
    },
    
    3: {
        "func": "app.order_trace.run",
        "describe": "[%s] 生成订单跟踪信息"
    },
    4: {
        "func": "app.user_setvip.run",
        "describe": "[%s] 批量设置会员"
    },
    5: {
        "func": "app.coord_update_mysql.run",
        "describe": "[%s] 获取经纬度"
    },
    
}

l = [select_map]

while True:

    handle_map = l[-1]
    print()
    for i in range(1, len(handle_map)-1):
        print(handle_map[i]['describe'] %i)

    if len(l) == 1:
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

        module_name, func_name = imp_name.rsplit('.', 1)

        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        func()

    elif a == 'q':
        break
