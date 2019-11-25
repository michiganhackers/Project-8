import RPi.GPIO as GPIO
import time

class EmergencyBrake(object):
    
    def __init__(self):
        self.throttle_coeff = 1.0
        self.stop_distance = 100
    def judge(self):
        stop = False
        if (distance < self.stop_distance):
            stop = True
        return stop
    
    def run(self, throttle, distance):
        print("EMERGENCY")
        stop = self.judge()
        if (stop == True):
            self.throttle_coeff = 0.0
        else:
            self.throttle_coeff = 1.0
        return throttle * self.throttle_coeff
            
            
        
