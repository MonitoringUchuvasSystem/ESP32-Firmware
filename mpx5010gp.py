from machine import ADC, Pin
from time import sleep_us

Cf = 1.5
Vs = 5

class analogPressure:
    def __init__(self):
        self.adc = ADC(Pin(33))
    
    def __preprocess__(self, data):
        Vout = (data*3.3)/65535
        P = Vout/(Vs*(3.6e-3))
        return P*Cf
    
    def read(self):
        return self.__preprocess__(self.adc.read_u16())