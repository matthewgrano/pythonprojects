import sys
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QPushButton)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer, QTime, Qt

class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.start_button = QPushButton("Start",self)
        self.stop_button = QPushButton("Stop",self)
        self.reset_button = QPushButton("Reset",self)
        self.timer = QTimer(self)
        self.time_label = QLabel("00:00:00.00",self)
        self.time = QTime(0,0,0,0)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Stopwatch")
        self.setGeometry(750,470,300,100)
        self.setWindowIcon(QIcon("stuff/stopwatch.png"))

        vbox = QVBoxLayout()

        vbox.addWidget(self.time_label)
        self.setLayout(vbox)

        hbox = QHBoxLayout()

        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)

        vbox.addLayout(hbox)

        self.time_label.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QPushButton, QLabel {
                padding: 20px;
                font-family: Arial;
            }
            QPushButton {
                font-size: 30px;
            }
            QLabel {
                font-size: 100px;
                border-radius: 20px;
            }
        """)

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.reset_button.clicked.connect(self.reset)
        self.timer.timeout.connect(self.updateTime)

    def start(self):
        self.timer.start(10)

    def stop(self):
        self.timer.stop()

    def reset(self):
        self.stop()
        self.time = QTime(0,0,0,0)
        self.time_label.setText(self.formatTime(self.time))

    def updateTime(self):
        self.time = self.time.addMSecs(10)
        self.time_label.setText(self.formatTime(self.time))

    def formatTime(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        ms = time.msec() // 10
        return f"{hours:02}:{minutes:02}:{seconds:02}.{ms:02}"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stopwatch = Stopwatch()
    stopwatch.show()
    exit(app.exec_())