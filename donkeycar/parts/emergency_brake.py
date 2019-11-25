import RPi.GPIO as GPIO
import time

class EmergencyBrake(object):
    
    def __init__(self):
        self.throttle_coeff = 1.0
        self.stop_distance = 100
    
    def judge(self,dist):
        distance = dist
        stop = False
        if (distance < self.stop_distance):
            stop = True
        return stop
    
    def run(self, throttle, dist):
        distance = dist
        stop = self.judge(distance)
        if (stop == True):
            self.throttle_coeff = 0.0
        else:
            self.throttle_coeff = 1.0
        print("coeff: ", self.throttle_coeff)
        return throttle * self.throttle_coeff
            
            
        
