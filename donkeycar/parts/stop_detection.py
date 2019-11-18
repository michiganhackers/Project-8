import time
import os
import cv2
import numpy as np

class StopSignDetector(object):
    def __init__(self):
        self.throttle_coeff = 1.0       # modify throttle
        self.max_dist = 50.0            # can be any value > 30.0
        self.slow_down_dist = 13.0      # when car starts slowing down
        self.stop_dist = 11.0           # when car has to stop
        self.stop_time = 2.5            # stop time in seconds
        self.have_stopped = False       # car has responded to the current stop
        self.to_sleep = False           # need to sleep this time
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
            print("x: ", x, " | y: " y, " | w: " w, " | h: ", h)
                
        return area
        
    # TODO
    def area_to_dist(self, area):
        '''
        return self.max_dist if area is 0, or
        return calculated distance based on area of
        bounding box.
        '''
        distance = self.max_dist
        if (area > 0):
            distance = 45.2 - 4.86 * np.log(area)
        return distance
    
    # TODO
    def dist_to_throttle_coeff(self, throttle_coeff, distance):
        '''
        return a new throttle coefficient based on
        current throttle coefficient and distance
        '''
        if (throttle_coeff > 0):
            return throttle_coeff - 0.05
        return throttle_coeff
        
    def run(self, throttle, image_array):
        distance = self.area_to_dist(self.stop_sign_detection(image_array))
        print("-- Distance: ", distance)
        if (self.to_sleep == True):
            print("Sleeping...")
#            time.sleep(self.stop_time)
            print("Wake up!")
            self.throttle_coeff = 1.0
            self.have_stopped = True
            self.to_sleep = False
            
        if (self.have_stopped == True):
            if (distance > self.slow_down_dist):         # stop sign out of scene
                self.have_stopped = False
            return throttle

        if (distance <= self.slow_down_dist):
            # start process if stop sign in range
            if (distance <= self.stop_dist):
                # stop immediately
                self.throttle_coeff = 0.0
                self.to_sleep = True
#            else:
#                # apply brake based on distance
#                self.throttle_coeff = self.dist_to_throttle_coeff(self.throttle_coeff, distance)
#                print("Throttle_coeff: ", self.throttle_coeff)
        print("== THROTTLE: ", throttle * self.throttle_coeff, " ==")
        
        try:
            return throttle * self.throttle_coeff
        except:
            print("throttle adjustment unsuccessful")
            return 0.0
    
    def shutdown(self):
        pass
