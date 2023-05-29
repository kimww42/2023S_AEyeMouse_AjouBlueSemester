from __future__ import division
import os
import cv2
import dlib
import csv
from .eye import Eye
from .calibration import Calibration
import pyautogui

class GazeTracking(object):
    """
    This class tracks the user's gaze.
    It provides useful information like the position of the eyes
    and pupils and allows to know if the eyes are open or closed
    """

    def __init__(self):
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()

        # _face_detector is used to detect faces
        self._face_detector = dlib.get_frontal_face_detector()

        # _predictor is used to get facial landmarks of a given face
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)
        self.left = []
        

    @property
    def pupils_located(self):
        """Check that the pupils have been located"""
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            # int(self.eye_right.pupil.x)
            # int(self.eye_right.pupil.y)
            return True
        except Exception:
            return False

    def _analyze(self):
        """Detects the face and initialize Eye objects"""
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)

        try:
            landmarks = self._predictor(frame, faces[0])
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            # self.eye_right = Eye(frame, landmarks, 1, self.calibration)


        except IndexError:
            self.eye_left = None
            # self.eye_right = None

    def refresh(self, frame):
        """
        Refreshes the frame and analyzes it.

        Arguments:
            frame (numpy.ndarray): The frame to analyze
        """
        self.frame = frame
        self._analyze()

    def pupil_left_coords(self):
        """Returns the coordinates of the left pupil"""
        if self.pupils_located:
            x = self.eye_left.origin[0] + self.eye_left.pupil.x
            y = self.eye_left.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def annotated_frame(self):
        """Returns the main frame with pupils highlighted"""
        frame = self.frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)
            x_left, y_left = self.pupil_left_coords()
            # x_right, y_right = self.pupil_right_coords()
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)

        return frame
    
    def move_mouse(self, eye_x, eye_y):
        '''참고 : https://seong6496.tistory.com/328'''
        
        if self.pupils_located:
            pyautogui.FAILSAFE = False
            # screen 1512*982
            width, height = pyautogui.size()

            # real input
            lja_data = [[-4, -4], [-1, -3], [2, -3], [6, -4], [12, -1],
                        [-3, -3], [-2, -4], [3, -3], [7, -3], [11, -1],
                        [-2, -2], [ 0, -1], [1, -1], [5, -1], [11,  0],
                        [-6,  0], [ 0,  0], [0,  0], [5,  1], [14,  3]]

            # cali input
            lja_cali_data = [[-4, -4], [0, -4], [4, -3], [8, -4], [12, -4],
                             [-4, -3], [0, -3], [4, -3], [8, -3], [12, -3],
                             [-4, -2], [0, -2], [4, -2], [8, -2], [12, -2],
                             [-4, -1], [0, -1], [4, -1], [8, -1], [12, -1],
                             [-4,  0], [0,  0], [4,  0], [8,  0], [12,  0]]

            gaze_x, gaze_y = self.pupil_left_coords()

            if eye_x or eye_y or gaze_x or gaze_y :
                x = (gaze_x - eye_x)
                y = (gaze_y - eye_y)

                if x < -4:
                    x = -4
                elif x > 12:
                    x = 12

                if y < -4:
                    y = -4
                elif y > 0:
                    y = 0

                x = x+4
                y = y+4
                print(x, y)
                width_scale = int(width/16)
                height_scale = int(height/4)
                print(width_scale, height_scale)
                x = width_scale * x
                y = height_scale * y
                print(f'{x}, {y}, eX:{eye_x}, eY:{eye_y}, gX:{gaze_x}, gY:{gaze_y}')
                pyautogui.moveTo(x, y)
