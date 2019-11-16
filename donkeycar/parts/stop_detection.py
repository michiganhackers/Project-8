import time
import os
import cv2
import numpy as np

class StopSignDetector(object):
    def __init__(self):
        self.throttle_coeff = 1.0       # modify throttle
        self.max_dist = 50.0            # can be any value > 30.0
        self.slow_down_dist = 30.0      # when car starts slowing down
        self.stop_dist = 10.0           # when car has to stop
        self.stop_time = 3.0            # stop time in seconds
        self.have_stopped = False       # car has responded to the current stop
        self.classifier = os.path.join(os.getcwd(), "cv/stopsign_classifier.xml")
    
    # TODO
    def stop_sign_detection(self, image_array):
        '''
        return 0 if no stop sign was detected, or
        return area of largest stop sign detected.
        '''
        clas = cv2.CascadeClassifier(classifier)
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        stop_signs = clas.detectMultiScale(image=gray, scaleFactor=1.02, minNeighbors=10)
        try:
            print(stop_signs)
        except:
            print("no sign found")
        
        area = 20.0
        return area
        
    # TODO
    def area_to_dist(self, area):
        '''
        return self.max_dist if area is 0, or
        return calculated distance based on area of
        bounding box.
        '''
        distance = 1 / area
        if (area == 0):
            distance = self.max_dist
        return distance
    
    # TODO
    def dist_to_throttle_coeff(self, throttle_coeff, distance):
        '''
        return a new throttle coefficient based on
        current throttle coefficient and distance
        '''
        brake = 1 / distance
        return throttle_coeff - 0.35 * brake
        
    def run(self, throttle, image_array):
        self.stop_sign_detection(image_array)
#        try:
#            stop_sign_detection(image_array)
#        except:
#            print("no image")
        
#        distance = self.area_to_dist(self.stop_sign_detection(image_array))
#        if (self.have_stopped == True):
#            if (distance > self.slow_down_dist):         # stop sign out of scene
#                self.have_stopped = False
#            return throttle
#
#        if (not self.have_stopped and distance <= self.slow_down_dist):
#            # start process if stop sign in range
#            if (distance <= self.stop_dist):
#                # stop immediately
#                self.throttle_coeff = 0.0
#                time.sleep(self.stop_time)
#                self.throttle_coeff = 1.0
#                self.have_stopped = True
#            else:
#                # apply brake based on distance
#                self.throttle_coeff = dist_to_throttle_coeff(self.throttle_coeff, distance)
        try:
            return throttle * 0.20
#            return throttle * self.throttle_coeff
        except:
            print("throttle adjust unsuccessful")
            return 0.0
    
    def shutdown(self):
        pass
