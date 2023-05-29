
from PyQt6.QtWidgets import *
import AEyeMouse
import tkinter as tk

root = tk.Tk()

if __name__ == "__main__":
    app = QApplication([])
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    width, height = screen_width, screen_height

    calibration = AEyeMouse.MainWindow(width, height, 1, 1)
    calibration.show()
    app.exec()
