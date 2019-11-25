import RPi.GPIO as GPIO
import time

class EmergencyBrake(object):
    
    def __init__(self):
        self.throttle_coeff = 1.0
        self.stop_distance = 100
        #set GPIO Pins
        self.GPIO_TRIGGER = 23
        self.GPIO_ECHO = 24
        #GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
        
    def distance(self):
        # set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()

        count = 0
        # save StartTime
        while GPIO.input(self.GPIO_ECHO) == 0:
            count += 1
            StartTime = time.time()
            print("c: ", count)
        
        # save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        print("TimeElapsed: ", TimeElapsed)
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        print("d: ", distance)
     
        return distance
    
    def judge(self):
        dist = self.distance()
        stop = False
        if (dist < self.stop_distance):
            stop = True
        return stop
    
    def run(self, throttle):
        print("EMERGENCY")
        stop = self.judge()
        if (stop == True):
            self.throttle_coeff = 0.0
        else:
            self.throttle_coeff = 1.0
        return throttle * self.throttle_coeff
            
            
        
