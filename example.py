"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
#!!

import cv2
from gaze_tracking import GazeTracking
import time
from gaze_tracking.blink_detect import Blink

gaze = GazeTracking()
blink = Blink()
webcam = cv2.VideoCapture(0)
clink = 0
count = 0


while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)    
    frame = gaze.annotated_frame()
    
    blink.refresh(frame)
    count = blink.detect_blink()
    
    #webcam에 좌우 눈동자 좌표를 text로 띄우는 부분
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    clink = blink.double_blink()
    
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (5, 25), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (5, 60), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Blink Count: " + str(count), (5, 105), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    if clink == 0:
        cv2.putText(frame, "Clink:" + 'no', (5, 150), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    elif clink == 1:
        cv2.putText(frame, "Clink:" + 'yes', (5, 150), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        
        
    cv2.imshow("Demo", frame)  
    
    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
