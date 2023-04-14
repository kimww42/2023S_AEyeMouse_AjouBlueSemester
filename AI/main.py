"""
virtualenv 환경에서 dlib importerror가 나는 관계로
conda 환경에서 실행.
"""
import math

import cv2
import dlib
import imutils

# 0이 기본 설정된 카메라.
capture = cv2.VideoCapture(0)

predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()

# opencv의 frame_width,height를 사용하면 기본적으로 카메라에서 지원되는 해상도로만 조절이 가능
# 그래서 imutils의 resize로 강제로 해상도를 바꿀 수 있음

"""
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # 가로
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # 세로
"""
def detect(gray, frame):
    faces = detector(frame)

    out_x = 0
    out_y = 0
    in_x = 0
    in_y = 0

    for face in faces:

        face_landmarks = predictor(gray, face)

        for n in range(0, 67):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y

            # 얼굴 외곽라인
            if(n < 17):
                out_x = out_x + face_landmarks.part(n).x / 17
                out_y = out_y + face_landmarks.part(n).y / 17
            # 얼굴 내부
            else:
                in_x = in_x + face_landmarks.part(n).x / 51
                in_y = in_y + face_landmarks.part(n).y / 51

            cv2.circle(frame, (x, y), 1, (0, 255, 0), 1)

        # print(in_x, in_y, out_x, out_y)
        cv2.circle(frame, (round(out_x), round(out_y)), 1, (0, 0, 255), 3)
        cv2.circle(frame, (round(in_x), round(in_y)), 1, (0, 0, 0), 3)
        # 얼굴 방향 계산
        theta = math.asin(2*(in_x-out_x) / (face.right() - face.left()))
        radian = theta*180/math.pi
        print('얼굴방향 {0:.3f} 각도 {1:.3f}도'.format(theta, radian))
        textShow = str(round(radian, 1))
        cv2.putText(frame, textShow, (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 1)
        # 왼쪽 눈과 오른쪽 눈의 중심점을 계산, 일단 왼쪽 눈을 기준으로 진행.
        left_eye = ((face_landmarks.part(36).x + face_landmarks.part(37).x + face_landmarks.part(38).x + face_landmarks.part(39).x + face_landmarks.part(40).x + face_landmarks.part(41).x) // 6,
                    (face_landmarks.part(36).y + face_landmarks.part(37).y + face_landmarks.part(38).y + face_landmarks.part(39).y + face_landmarks.part(40).y + face_landmarks.part(41).y) // 6)
        # right_eye = ((face_landmarks.part(42).x + face_landmarks.part(45).x) // 2, (face_landmarks.part(42).y + face_landmarks.part(45).y) // 2)

        # 중심점을 표시
        cv2.circle(frame, left_eye, 2, (0, 0, 255), -1)
        # cv2.circle(frame, right_eye, 2, (0, 0, 255), -1)


while True:
    # 영상을 받아오지 못할 경우, retval은 false로 return.
    retval, frame = capture.read()
    # 좌우 반전
    frame = cv2.flip(frame, 1)
    # 이미지 크기를 줄이고, 흑백으로 변환하여 계산 시간을 줄임
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)

    detect(gray, small_frame)

    if not retval:
        print("couldn't read frames")
    else:
        cv2.imshow("AEyeMouse", small_frame)

    # ESC(27) 누르면 break
    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
cv2.destroyAllWindows()
