"""
virtualenv 환경에서 dlib importerror가 나는 관계로
conda 환경에서 실행.
"""
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
    for face in faces:

        face_landmarks = predictor(gray, face)

        for n in range(0, 67):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y

            cv2.circle(frame, (x, y), 1, (0, 255, 0), 1)

while True:
    # 영상을 받아오지 못할 경우, retval은 false로 return.
    retval, frame = capture.read()
    # 좌우 반전
    frame = cv2.flip(frame, 1)
    # 해상도 변경
    frame = imutils.resize(frame, width=1920)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detect(frame, frame)

    if not retval:
        print("couldn't read frames")
    else:
        cv2.imshow("AEyeMouse", frame)

    # ESC(27) 누르면 break
    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
cv2.destroyAllWindows()
