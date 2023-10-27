from machine import ADC, Pin
from time import sleep_us
import time


class MHZ14A:
    def __init__(self):
        self.adc = ADC(Pin(32))
    
    def __preprocess__(self, data):
        Vout = ((data*3.25)/65535)-1.3
        P = int((Vout-0.4) * (5000/(2-0.4)))
        return P
    
    def read_co2(self):
        return self.__preprocess__(self.adc.read_u16())