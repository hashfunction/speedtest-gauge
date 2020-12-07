import time
import RPi.GPIO as GPIO
import board

class Button:
    pin = 10 

    def WaitForPress(self, timeout):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
        return GPIO.wait_for_edge(self.pin, GPIO.RISING, timeout = timeout)

    def Complete(self):
        GPIO.cleanup()

