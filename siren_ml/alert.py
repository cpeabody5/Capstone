from gpiozero import LED

class Alerter():
    def __init__(self, gpio_num = 17):
        self.led = LED(gpio_num)
    
    def set_alert_status(self, alert):
        if alert:
            self.led.on()
        else:
            self.led.off()