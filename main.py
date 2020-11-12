# imports
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QSizePolicy, QFileDialog, QMenu, QStyle
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt, QUrl, QPoint

SCREEN_SIZE = [800, 600]

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Задаём размер и название окна
        self.setGeometry(350, 100, *SCREEN_SIZE)
        self.setWindowTitle('VideoPlayer')

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.initUI()

        self.show()

    def initUI(self):
        # Creating mediaPlayer
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Creating PushButton to Play
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # Creating PushButton to Open Video
        oBtn = QPushButton('Open Video')
        oBtn.clicked.connect(self.open_file)

        # Creating Label
        self.label = QLabel()

        # Make sure that the slider is at the bottom
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Creating videoWidget
        videowidget = QVideoWidget()

        # Creating Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # Creating Hbox
        HboxLayout = QHBoxLayout()
        HboxLayout.setContentsMargins(0, 0, 0, 0)

        # Combining Widgets in a Hbox
        HboxLayout.addWidget(oBtn)
        HboxLayout.addWidget(self.playBtn)
        HboxLayout.addWidget(self.slider)

        # Creating Vbox
        VboxLayout = QVBoxLayout()

        # Combining Widgets in a Vbox
        VboxLayout.addWidget(videowidget)
        VboxLayout.addLayout(HboxLayout)
        VboxLayout.addWidget(self.label)

        # Add Video Output on widget
        self.mediaPlayer.setVideoOutput(videowidget)

        self.setLayout(VboxLayout)

        # Triggers
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        self.mediaPlayer.error.connect(self.handle_errors)

    # function to open video from computer
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        self.playBtn.setEnabled(True)

    # function to play/pause video
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    # function to change icon on play button
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    # position tracking
    def position_changed(self, position):
        self.slider.setValue(position)

    # duration tracking
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    # function to change position
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    # Custom errors
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoPlayer()
    ex.show()
    sys.exit(app.exec())