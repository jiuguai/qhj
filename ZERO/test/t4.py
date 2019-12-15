class OrderEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        
        if isinstance(obj, datetime.datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S')  
        else:
            return super(MyEncoder, self).default(obj)
    js = json.dumps(row.to_dict(),cls=OrderEncoder,ensure_ascii=False)

    order_num = row['订单号']
    spp_num = row['发货商ID']