from manager import Kernel
from machine import Timer, RTC
import network
import ntptime
import time

ssid = "dlink-0B4C"
password = "sWkADc:nHzxX-K|o&mnIbnw24"
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

timeout = 30

connected = False
start_time = time.ticks_ms()

while not connected and time.ticks_diff(time.ticks_ms(), start_time) < timeout * 1000:
    wifi.connect(ssid, password)
    while not wifi.isconnected():
        time.sleep(1)
    if wifi.isconnected():
        connected = True
        
mang = Kernel()
tim1 = Timer(1)

if connected:
    ntptime.settime()
    (year, month, mday, week_of_year, hour, minute, second, milisecond)=RTC().datetime()
    RTC().init((year, month, mday, week_of_year, hour-5, minute, second, milisecond))
    
    tim1.init(period=12000, mode=Timer.PERIODIC, callback=lambda _: mang.read())