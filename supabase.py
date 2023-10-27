import urequests as requests
from time import sleep
import machine, time

url = 'http://uchuvasensor.pythonanywhere.com/supabase'

class Sender(object):
    def __init__(self):
        self.fatal_error_count = 0
        
    def __post__(self, data):
        pyload = {'data': data}
        resp = requests.post(url, json=pyload)
        return resp.status_code
                

    def __send__(self, data, mode=0):
        if mode == 0:
            resp = self.__post__(','.join(str(value) for value in data))
            print(resp)

    def send(self, data):
        print(data)
        try:
            self.__send__(data, mode = 0)
        except:
            self.fatal_error_count +=1
        
        if self.fatal_error_count > 3:
            self.fatal_error_count = 0
            machine.reset()
            
            
            
            
            
            
            