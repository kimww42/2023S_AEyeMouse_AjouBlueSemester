from __future__ import division
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import imutils
import cv2
import dlib
import os

class Blink(object):
    
    def __init__(self):
        self.frame = None
        self.eye = 0
        self.rects = []
        self.counter = 0
        self.double = 0
        self.total = 0
        self.leftEye = []
        self.rightEye = []
        
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self.predictor = dlib.shape_predictor(model_path)
        self.detector = dlib.get_frontal_face_detector()
        
    def refresh(self, frame):
        self.frame = frame
        self._analyze()
        
    def _analyze(self):
        frame = imutils.resize(self.frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.rects = self.detector(gray, 0)
        
    def eye_aspect_ratio(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])

        ear = (A + B) / (2.0 * C)
        return ear
    
    def detect_blink(self):        
        frame = imutils.resize(self.frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
        
        EYE_AR_THRESH = 0.25
        EYE_AR_CONSEC_FRAMES = 3
        
        for rect in rects:
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            self.leftEye = shape[lStart: lEnd]
            self.rightEye = shape[rStart: rEnd]
            print(self.leftEye)
            leftEAR = self.eye_aspect_ratio(self.leftEye)
            rightEAR = self.eye_aspect_ratio(self.rightEye)

            self.ear = (leftEAR + rightEAR) / 2.0
            
            if self.ear < EYE_AR_THRESH:
                self.counter += 1
            else:
                if self.counter >= EYE_AR_CONSEC_FRAMES:
                    self.total += 1     #blink count
                self.counter = 0
                return self.total
            
    '''===============================이 부분을 우짜지============================'''
    def double_blink(self):
        if self.total % 2 == 0:
            self.double = 0
            return 1
        else:
            return 0