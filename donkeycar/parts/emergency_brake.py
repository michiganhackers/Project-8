import RPi.GPIO as GPIO
import time

class EmergencyBrake(object):
    
    def __init__(self):
        self.throttle_coeff = 1.0
        self.stop_distance = 100
        stop = False
        #set GPIO Pins
        self.GPIO_TRIGGER = 18
        self.GPIO_ECHO = 24
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        
    def distance(self):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
     
        return distance
    
    def judge(self):
        dist = self.distance()
        if (dist < stop_distance):
            stop = True
        return stop
    
    def run(self, throttle):
        stop = self.judge()
        if (stop == True):
            self.throttle_coeff = 0.0
        else:
            self.throttle_coeff = 1.0
        return throttle * self.throttle_coeff
            
            
        