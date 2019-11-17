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
        self.stop_time = 1.0            # stop time in seconds
        self.have_stopped = False       # car has responded to the current stop
        self.classifier = os.path.join("/home/pi/projects/Project-8/donkeycar/parts/cv/stopsign_classifier.xml")
    
    # TODO
    def stop_sign_detection(self, image_array):
        '''
        return 0 if no stop sign was detected, or
        return area of largest stop sign detected.
        '''
        area = 0
        if image_array is not None:
            classifier = cv2.CascadeClassifier(self.classifier)
            image_array_np = np.array(image_array)
            gray = cv2.cvtColor(image_array_np, cv2.COLOR_BGR2GRAY)
            stop_signs = classifier.detectMultiScale(image=gray, scaleFactor=1.02, minNeighbors=10)
            print(len(stop_signs), "STOP signs found.")
            for (x, y, w, h) in stop_signs:
                area = max(w * h, area)
            print("area: ", area)
                
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
        return 25
    
    # TODO
    def dist_to_throttle_coeff(self, throttle_coeff, distance):
        '''
        return a new throttle coefficient based on
        current throttle coefficient and distance
        '''
        brake = 1 / distance
        return throttle_coeff - 0.01
        
    def run(self, throttle, image_array):
    
        distance = self.area_to_dist(self.stop_sign_detection(image_array))
        if (self.have_stopped == True):
            if (distance > self.slow_down_dist):         # stop sign out of scene
                self.have_stopped = False
            return throttle

        if (not self.have_stopped and distance <= self.slow_down_dist):
            # start process if stop sign in range
            if (distance <= self.stop_dist):
                # stop immediately
                self.throttle_coeff = 0.0
                print("Sleeping...")
                time.sleep(self.stop_time)
                print("Wake up!")
                self.throttle_coeff = 1.0
                self.have_stopped = True
            else:
                # apply brake based on distance
                print("Throttle_coeff: ", self.throttle_coeff)
                self.throttle_coeff = dist_to_throttle_coeff(self.throttle_coeff, distance)
        
        
        print("== THROTTLE: ", throttle * self.throttle_coeff, " ==")
        try:
            return throttle * self.throttle_coeff
        except:
            print("throttle adjustment unsuccessful")
            return 0.0
    
    def shutdown(self):
        pass
