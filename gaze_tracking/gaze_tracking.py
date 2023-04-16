from __future__ import division
import os
import cv2
import dlib
from .eye import Eye
from .calibration import Calibration


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
        self.count = 0
        self.double_blink = False
        

    @property
    def pupils_located(self):
        """Check that the pupils have been located"""
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            int(self.eye_right.pupil.x)
            int(self.eye_right.pupil.y)
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
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)

        except IndexError:
            self.eye_left = None
            self.eye_right = None

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

    def pupil_right_coords(self):
        """Returns the coordinates of the right pupil"""
        if self.pupils_located:
            x = self.eye_right.origin[0] + self.eye_right.pupil.x
            y = self.eye_right.origin[1] + self.eye_right.pupil.y
            return (x, y)

    def annotated_frame(self):
        """Returns the main frame with pupils highlighted"""
        frame = self.frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)
            x_left, y_left = self.pupil_left_coords()
            x_right, y_right = self.pupil_right_coords()
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)

        return frame
    
    ##################################################################################################################
    '          ************************************    여기 보세요    **********************************              '
    ##################################################################################################################
    
    def left_eye(self):
        '''
        return left eye's coordinate(x,y) and whether left eye's double blinking
        if user blinks twice, double_blink will be returned as 1       
        '''
        left_x = left_y = 0
        self.double_blink = False
        
        if self.pupils_located:       
            left_x, left_y = self.pupil_left_coords()    
                            
            # #blinking 기존 코드
            # blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            # if blinking_ratio > 3.8:    #3.8
            #     blink = 1          
            
        '''
        원래 detect_blink.py 코드로 blink 횟수 파악해서 2번 깜박이면 click signal 발생시키도록 해야하는데
        그렇게 하려면 오늘만에 못할거 같아서 일단 무식하게 방법으로 구현만 해놨어
        이번주 틈틈이+시험 끝나고 해서 수정해놓겠습니다 하ㅏ핳ㅎ하  
        '''
        if left_x == 0 and left_y == 0:
            self.count += 1
            
        if self.count >= 6 and self.count <= 8:
            self.count = 0
            self.double_blink = 1
        
        return left_x, left_y, self.double_blink
        
    ##################################################################################################################
