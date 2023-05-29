from PyQt6 import *
import time
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Tracker(QThread):
    my_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            result = "finish"
            # 메인 스레드로 값 전달 전달
            self.my_signal.emit(result)
            time.sleep(2)

class CircleWidget(QWidget):
    def __init__(self, parent=None):
        super(CircleWidget, self).__init__(parent)
        self.circle_color = QColor(255, 0, 0)  # 원의 색상을 설정합니다

    def paintEvent(self, event):
        painter = QPainter(self)

        # 현재 위젯의 크기를 가져옵니다
        width = self.width()
        height = self.height()

        # 가로로 원 그리기
        painter.setPen(QPen(self.circle_color, 3, QtCore.Qt.PenStyle.SolidLine))
        painter.drawEllipse(0, 0, 80, 80)
        painter.drawEllipse(0, height-int(height*0.07), 80, 80)
        painter.drawEllipse(width-int(width*0.04), 0, 80, 80)
        painter.drawEllipse(width-int(width*0.04), height-int(height*0.07), 80, 80)


class CaliWindow(QMainWindow):
    def __init__(self, w, h):
        super(CaliWindow, self).__init__()

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)  # 타이틀바 제거 + 항상 위에

        self.setGeometry(0, 0, w, h)
        self.setWindowTitle("Eye Track Pos Calculation")

        self.circle_widget = CircleWidget()
        self.setCentralWidget(self.circle_widget)

        self.resize(w, h)


class MainWindow(QtWidgets.QWidget):
    def __init__(self, w, h, x, y):
        super().__init__()

        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint | QtCore.Qt.WindowType.WindowStaysOnTopHint)  # 타이틀바 제거 + 항상 위에
        self.setAttribute(QtCore.Qt.WindowType.WA_TranslucentBackground)  # 백그라운드를 없애버림

        # 버튼 생성
        self.dBtn = DoubleClick()
        self.dBtn.setText("Double Click")

        self.rBtn = MouseButton()
        self.rBtn.setText("Right Click")

        self.wBtn = WheelClick()
        self.wBtn.setText("Wheel Click")

        self.lBtn = LeftClick()
        self.lBtn.setText("Left Click")

        self.drBtn = Drag()
        self.drBtn.setText("Drag")

        self.eBtn = onExit(self)
        self.eBtn.setText("Exit")

        layout = QtWidgets.QGridLayout(self)
        self.setLayout(layout)

        layout.addWidget(self.lBtn, 0, 0)
        layout.addWidget(self.wBtn, 0, 1)
        layout.addWidget(self.rBtn, 0, 2)
        layout.addWidget(self.dBtn, 2, 0)
        layout.addWidget(self.drBtn, 2, 1)
        layout.addWidget(self.eBtn, 2, 2)

        # 멀티 쓰레딩
        self.Tracker = Tracker()
        self.Tracker.my_signal.connect(self.control_mouse)
        self.Tracker.start()

        self.resize(int(w / 6), int(h / 6))
        self.move(x - int(w / x), y)

    def control_mouse(self, result):
        if result == "Double Blink":
            print(f"{result} 마우스 제어")


class MouseButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        #  특정 시간 올리면 작동되도록 버튼에 타이머 삽입 -> 드웰링시 작동되도록 수정할 것
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_timeout)

        self.setMinimumSize(10, 50)
        self.resize(20, 60)
        self.setContentsMargins(0, int(self.size().width()), 0, int(self.size().height()))
        # 각자 변경하고 싶은 색상의 헥사코드를 입력
        self.color1 = QtGui.QColor('#FFFF00')
        self.color2 = QtGui.QColor('#FFFFFF')

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.0001,
            endValue=0.9999,
            duration=3000  # duration 인자로 색상 변경 시간을 millisecond 단위로 설정함 (0.25초)
        )

        self.clicked.connect(self.doEvent)

    def _animate(self, value):
        qss = '''
            font: 75 10pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(0, 0, 0);
            border-style: solid;
            border-radius: 10px;
        '''

        grad = f'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 ' \
               f'{self.color1.name()}, stop:{value} {self.color2.name()}, stop: 1.0 {self.color1.name()})'

        qss += grad
        self.setStyleSheet(qss)

    def doEvent(self, event):
        self.timer.start(3000)
        self.setEnabled(False)
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()

    def on_timeout(self):
        self.setEnabled(True)
        pyautogui.click(button="right")


class DoubleClick(MouseButton):
    def on_timeout(self):
        self.setEnabled(True)


class LeftClick(MouseButton):
    def on_timeout(self):
        self.setEnabled(True)


class Drag(MouseButton):
    def on_timeout(self):
        self.setEnabled(True)


class Keyboard(MouseButton):
    def on_timeout(self):
        self.setEnabled(True)
        print("아직 미구현")


class WheelClick(MouseButton):
    def on_timeout(self):
        self.setEnabled(True)


class onExit(MouseButton):
    def __init__(self, window, parent=None):
        super().__init__(parent)

        #  특정 시간 올리면 작동되도록 버튼에 타이머 삽입 -> 드웰링시 작동되도록 수정할 것
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.on_timeout)

        self.window = window

        self.setMinimumSize(10, 50)
        self.resize(20, 60)
        self.setContentsMargins(0, int(self.size().width()), 0, int(self.size().height()))
        # 각자 변경하고 싶은 색상의 헥사코드를 입력
        self.color1 = QtGui.QColor('#FFFF00')
        self.color2 = QtGui.QColor('#FFFFFF')

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.0001,
            endValue=0.9999,
            duration=3000  # duration 인자로 색상 변경 시간을 millisecond 단위로 설정함 (0.25초)
        )

        self.clicked.connect(self.doEvent)

    def _animate(self, value):
        qss = '''
            font: 75 10pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(0, 0, 0);
            border-style: solid;
            border-radius: 10px;
        '''

        grad = f'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 ' \
               f'{self.color1.name()}, stop:{value} {self.color2.name()}, stop: 1.0 {self.color1.name()})'

        qss += grad
        self.setStyleSheet(qss)

    def doEvent(self, event):
        self.timer.start(0)

    def on_timeout(self):
        self.window.close()
