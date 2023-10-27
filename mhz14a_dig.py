import machine

class MHZ14A_DIG:
    def __init__(self):
        self.pin_1 = machine.Pin(16, machine.Pin.IN)
        self.pin_1.irq(trigger=machine.Pin.IRQ_RISING, handler=self.on_rising_edge_1)
        self.pin_1_time = 0

        self.pin_0 = machine.Pin(17, machine.Pin.IN)
        self.pin_0.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.on_falling_edge_0)
        self.pin_0_time = 0

    def on_rising_edge_1(self, pin):
        self.pin_1_time = machine.time_pulse_us(pin, 1)

    def on_falling_edge_0(self, pin):
        self.pin_0_time = machine.time_pulse_us(pin, 0)

    def get_high_time(self):
        return self.pin_1_time

    def get_low_time(self):
        return self.pin_0_time
    
    def get_co2(self):
        high_time = self.get_high_time()/1000
        low_time = self.get_low_time()/1000
        return int(5000*((high_time-2)/(high_time+low_time-4)))