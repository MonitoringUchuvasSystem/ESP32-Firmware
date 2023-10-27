from mpx5010gp import analogPressure
from machine import (SoftI2C, Pin)
from mhz14a_dig import MHZ14A_DIG
from supabase import Sender
from bmp280 import BMP280
from mhz14a import MHZ14A
import time

class Kernel(object):
    def __init__(self):
        self.sender = Sender()
        self.__init__mhz14a__()
        self.__bmp280_config__()
        self.__init_mpx5010gp__()
        self.__init__mhz14a_dig__()
        self.pilot = Pin(2, Pin.OUT)
        self.pilot.off()

    def __bmp280_config__(self):
        bus = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.bmp = BMP280(bus)
        self.bmp.normal_measure()
    
    def __init_mpx5010gp__(self):
        self.mpx = analogPressure()
    
    def __init__mhz14a__(self):
        self.co2 = MHZ14A()
    
    def __init__mhz14a_dig__(self):
        self.co2_dig = MHZ14A_DIG()
        
    def __bmp280_read__(self):
        return self.bmp.temperature, self.bmp.pressure
    
    def __mpx5010gp_read__(self):
        return self.mpx.read()
    
    def __mhz14a_read__(self):
        self.ppm = self.co2.read_co2()
        if self.ppm > 0:
            return self.ppm
        else:
            return -1

    def __datetime__(self, st):
        datetime = "{:4}-{:2}-{:02d} {:2}:{:02d}:{:02d}".format(st[0], st[1], st[2], st[3], st[4], st[5])
        try: datetime = datetime.replace('- ','-')
        except: pass
        return datetime

    def read(self):
        mhz = -1
        self.pilot.on()
        try:
            datetime = self.__datetime__(time.localtime())
            while mhz < 0 and mhz < 5000: mhz = self.co2_dig.get_co2() #self.__mhz14a_read__()
            mpx = self.__mpx5010gp_read__()
            bmp = self.__bmp280_read__()
            self.sender.send([bmp[0], bmp[1]/1000, mpx, mhz, datetime])
        except: pass
        self.pilot.off()





