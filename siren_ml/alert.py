from gpiozero import LED

class Alerter():
    def __init__(self, alert_gpio_num = 17, status_gpio_num = 23):
        self.led = LED(alert_gpio_num)
        self.status = LED(status_gpio_num)
    
    def set_alert_status(self, alert):
        if alert:
            self.led.on()
        else:
            self.led.off()
    
    def set_system_status(self, status):
        if status:
            self.status.on()
        else:
            self.status.off()
    

