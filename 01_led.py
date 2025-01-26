from gpiozero import LED
import time
led = LED(17)
while True:
    led.on()S
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)
