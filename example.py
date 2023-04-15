"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""
#!!

import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
left_x, left_y, blink  = 0, 0, 0

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)
    
    
    ##################################################################################################################
    '          ************************************    여기 보세요     **********************************             '
    
    left_x, left_y, blink = gaze.left_eye()
    print(left_x, left_y, blink)
    
    ##################################################################################################################


    #webcam에 좌우 눈동자 좌표를 text로 띄우는 부분
    frame = gaze.annotated_frame()

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (5, 25), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (5, 60), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)  
    
    if cv2.waitKey(1) == 27:
        break
   
webcam.release()
cv2.destroyAllWindows()
