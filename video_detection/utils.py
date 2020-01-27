import cv2
import threading
import os
import math
import random
import base64
from ctypes import *

class RecordingThread(threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.is_running = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi', fourcc, 20.0, (640,480))

    def run(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.is_running = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self, camera, alert_classes):
        # Open a camera
        self.cap = cv2.VideoCapture(camera)
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recording_thread = None
        self.alert_classes = set(alert_classes)
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self, byte=False):
        ret, frame = self.cap.read()

        if not ret:
            return None

        if byte:
            frame = cv2.resize(frame, (360, 270))
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            return frame

    def start_record(self):
        self.is_record = True
        self.recording_thread = RecordingThread("Video Recording Thread", self.cap)
        self.recording_thread.start()

    def stop_record(self):
        self.is_record = False

        if self.recording_thread != None:
            self.recording_thread.stop()

    def draw_yolo(self, detected_objects):
        color = {
            'glass':(0, 0, 254),
            'plastic':(0,254,0),
            'can':(254,0,0)
        }
        frame = self.get_frame(False)
        is_detected_alert_class = False

        for obj, confidence, rect in detected_objects:
            x, y, w, h = rect
            w, h = round(w), round(h)
            x1, y1 = int(x-w/2), int(y-h/2)
            x2, y2 = x1+w, y1+h
            detected_class = obj.decode('utf-8')
            text = '{} {}%'.format(detected_class, round(confidence*100))
            
            if detected_class in self.alert_classes:
                is_detected_alert_class = True
            #     frame = cv2.rectangle(frame, (x1, y1), (x2, y2), color[detected_class], 3)

            # else:
            #     frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 2)
            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), color[detected_class], 3)

            frame = cv2.putText(frame, text, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), lineType=cv2.LINE_AA)

        frame = cv2.resize(frame, (360, 270))
        ret, jpeg = cv2.imencode('.jpg', frame)

        jpeg_bytes = jpeg.tobytes()

        return base64.b64encode(jpeg_bytes), is_detected_alert_class
