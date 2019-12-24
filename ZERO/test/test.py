names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
values =[820, 932, 901, 934, 1290, 1330, 1320]

items = dict(zip(names,values))
data = []
for k,v in items.items():
    d = {
        "name":k,
        "value":v
    }
    
    data.append(d)

print(data)