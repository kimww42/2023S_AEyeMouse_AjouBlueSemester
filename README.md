# 2023S_AEyeMouse_AjouBlueSemester
<img src="https://user-images.githubusercontent.com/23449575/228896765-89614653-7140-4922-8972-de81f9dc15e2.png" width="10%" height="10%">
아주대학교 파란학기제(2023S) 미키마우스팀의 도전과제 AEyeMouse입니다.
<br><br>

## Ai 방향성 정리
### issue #1

<b>Face Alignment(Face landmark detection)</b><br>
Face Alignment란? face detection 이후 얼굴의 특정 지점에 landmark를 부여하는 작업. 얼굴 특징점 검출이라고 함.<br>

Face Alignment를 진행하여 User의 눈이 어느 곳에 위치하는 지를 알아내는 것이 첫 번째 과제.<br>
<b>왜?</b><br>단순히 화면 상에서 동공이 어느 곳에 위치하느냐로는 어느 곳을 쳐다보는 지 알 수 없음.<br>같은 곳을 쳐다봐도 얼굴이 움직이면 눈의 위치, 동공의 위치는 바뀌기 때문.<br>
그래서 눈의 중앙점을 구하고, 동공의 위치를 구해 눈의 중앙점과 동공의 위치의 차이로 쳐다보는 좌표를 구해야 함.

Face Alignment를 통해 얼굴의 크기를 알아내는 것이 두 번째 과제.<br>
<b>왜?</b><br>단순히 첫 번째 과제로만 좌표를 구하게 되면 얼굴이 카메라에서 가까워졌을 때와 멀어졌을 때 대응할 수 없음.<br>얼굴이 카메라에서 가까워지면 동공 위치의 변화도 더 커지기 때문에 이를 보정하는 알고리즘을 작성하기 위해 얼굴의 크기를 알아내야 함.

### issue #2

<b>Pupil Detection</b><br>
앞선 Face Alignment로 눈의 위치를 찾아냈기 때문에 이를 이용해 동공을 detect해야 함.<br>

동공을 detect하여 동공의 위치를 좌표화하는 것에 성공한다면 끝인가?

------------
[팀 Facebook](https://www.facebook.com/%EC%95%84%EC%A3%BC%EB%8C%80%ED%95%99%EA%B5%90-%ED%8C%8C%EB%9E%80%ED%95%99%EA%B8%B0-%EB%AF%B8%ED%82%A4%EB%A7%88%EC%9A%B0%EC%8A%A4-104675412575605)
