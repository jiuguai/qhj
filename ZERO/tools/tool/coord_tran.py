
import requests
from ..settings.web_map import *
from ..custom_exception import ServiceError
class KeyField():
    def __get__(self,instance, owner):

        return instance.__key
    def __set__(self, instance, value):
        instance.__key = value
        instance.params = {
            "key":value
        }
    def __delete__(self, instance):

        del instance.__key

class GeoAPIField():
    def __get__(self,instance, owner):

        return instance.__api

    def __set__(self, instance, api_name):
        instance.__api = api_name


        instance.geo_url = GEO_URL[api_name]
        instance.handle_func = getattr( instance,instance.__class__.handles[api_name]['handle'])

    def __delete__(self, instance):

        del instance.__key


class ReGeoAPIField():
    def __get__(self,instance, owner):

        return instance.__api

    def __set__(self, instance, api_name):
        instance.__api = api_name


        instance.regeo_url = REGEO_URL[api_name]
        instance.handle_func = getattr( instance,instance.__class__.handles[api_name]['handle'])

    def __delete__(self, instance):

        del instance.__key


class ReGeo():
    key = KeyField()
    api = ReGeoAPIField()
    handles = {
        "baidu":{
            "handle":"_ReGeo__baidu_regeo"
        },
        "gaode":{
            "handle":"_ReGeo__gaode_regeo"
        }
    }
    def __init__(self, api_name="gaode"):

        
        self.key = WEB_KEYS[api_name]

        self.api = api_name


    def __gaode_regeo(self):

        self.params['lng'] = self.lng
        self.params['lat'] = self.lat
        url = self.regeo_url.format(**self.params)

        rep = requests.get(url)

        result = rep.json()
        
        if result['status'] == "0":
            raise ServiceError(",lng%s ,lat:%s , 服务器异常无法查询地址" %(self.lng,self.lat),self)


        address_component = result['regeocode']['addressComponent']
        street_number = address_component['streetNumber']
        street = street_number['street']
        formatted_address = result['regeocode']['formatted_address']
#         print(result)
        self.item = { '国家':address_component['country'], 
                '省份':address_component['province'],
                '城市':address_component['province'] if isinstance(address_component['city'], list) else  address_component['city'],  
                '县区':address_component['district'], 
                '街道':street_number['street'],
                'lng':self.lng,
                'lat':self.lat,
               '格式化地址':formatted_address}
    

    def __baidu_regeo(self):
        self.params['lng'] = self.lng
        self.params['lat'] = self.lat

        
        rep = requests.get(self.regeo_url.format(**self.params))
        result = rep.json()
        
        if result['status']:
            raise ServiceError("lat:%s, lng%s 服务器异常无法查询地址" %(self.lat,self.lng),self)
        # raise ServiceError("lat:%s, lng%s 服务器异常无法查询地址" %(self.lat,self.lng),self)
            
        result = result['result']
        address_component = result['addressComponent']

        formatted_address = result['formatted_address']
        #         print(result)
        self.item = { '国家':address_component['country'], 
                '省份':address_component['province'],
                '城市':address_component['city'],  
                '县区':address_component['district'], 
                '街道':address_component['street'],
                'lng':self.lng,
                'lat':self.lat,
                
               '格式化地址':formatted_address}


    def __call__(self, *args, **kargs):

        self.regeo(*args, **kargs)


        return self


    def regeo(self, *args, **kargs):



        if len(args) == 2:
            self.lng = args[0]
            self.lat = args[1]
        if 'lng' in kargs and 'lat' in kargs:
            self.lng = kargs.get('lng')
            self.lat = kargs.get('lat')
            
        if not ('lng' in self.__dict__ and 'lat'in self.__dict__):
            raise TypeError("miss lng or lat")
        
        self.handle_func()
        
        return self





class Geo():
    key = KeyField()
    api = GeoAPIField()

    handles = {
        "baidu":{
            "handle":"_Geo__baidu_geo"
        },
        "gaode":{
            "handle":"_Geo__gaode_geo"
        }
    }
    def __init__(self, api_name='gaode'):

        self.key = WEB_KEYS[api_name]

        self.api = api_name

    def __call__(self, *args, **kargs):

        self.geo(*args, **kargs)

        return self

    def geo(self, *args, **kargs):

        if len(args) == 1:
            self.addr = args[0]
        if 'address' in kargs:
            self.addr = kargs.get('address')
        
        if 'addr' not in self.__dict__:
            raise TypeError("miss address")
        self.params['address'] = self.addr

        # self.__gaode_geo()
        # self.__baidu_geo()
        self.handle_func()

        return self

    def __gaode_geo(self):
        url = self.geo_url.format(**self.params)

        rep = requests.get(url)

        result = rep.json()

        if result['status'] == "0":
           raise ServiceError("%s ： \n无法获取坐标" %self.addr,self)

        self.location = result['geocodes'][0]['location'].split(',')

        self.lng = self.location[0]
        self.lat = self.location[1]
        self.location = {'lng':self.lng, 'lat':self.lat}
   
    def __baidu_geo(self):

        rep = requests.get(self.geo_url.format(**self.params))

        result = rep.json()
        if result['status']:
           raise ServiceError("%s ： \n无法获取坐标" %self.addr,self)
        self.location = result['result']['location']
        self.lng = self.location['lng'] 
        self.lat = self.location['lat']



