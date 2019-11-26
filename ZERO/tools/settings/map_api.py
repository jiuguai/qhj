WEB_KEYS = {
    "baidu":'pKthM9TxiqPsGx81IAwlkVuGRphmwdDR',
        
    "gaode":'138942d50e3bee60df440472c9ae123f',
}


GEO_URL = {
    "baidu":"http://api.map.baidu.com/geocoding/v3/?address={address}s&ret_coordtype=gcj02ll&output=json&ak={key}",

    "gaode":"https://restapi.amap.com/v3/geocode/geo?address={address}&key={key}",
}


RGEO_URL = {
    "baidu":"http://api.map.baidu.com/reverse_geocoding/v3/?ak={key}&output=json&coordtype=gcj02ll&location={lat},{lng}",
    
    "gaode":"https://restapi.amap.com/v3/geocode/regeo?location={lng},{lat}&radius=1000&extensions=all&key={key}",
}