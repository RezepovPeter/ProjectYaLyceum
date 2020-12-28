# импорты
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider,\
    QSizePolicy, QFileDialog, QMenu, QStyle, QShortcut
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPalette, QIcon, QKeySequence
from PyQt5.QtCore import Qt, QUrl, QPoint

# размер окна
SCREEN_SIZE = [800, 600]


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # ставим окошко
        self.setGeometry(350, 100, *SCREEN_SIZE)
        # меняем название
        self.setWindowTitle('VideoPlayer')

        # создаём палет
        p = self.palette()
        # заливаем чёрным
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        # быстрые клавиши
        # открытие файла
        self.shortcut = QShortcut(QKeySequence("o"), self)
        self.shortcut.activated.connect(self.open_file)
        # пауза
        self.shortcut = QShortcut(QKeySequence(" "), self)
        self.shortcut.activated.connect(self.play_video)
        # полный экран
        self.shortcut = QShortcut(QKeySequence("f"), self)
        self.shortcut.activated.connect(self.handleFullscreen)
        # на 1 минуту дальше
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forwardSlider)
        # на 1 минуту раньше
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backSlider)
        # +10% звука
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.shortcut.activated.connect(self.volumeUp)
        # -10% звука
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.shortcut.activated.connect(self.volumeDown)
        # вперёд на 10 минут
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forwardSlider10)
        # назад на 10 минут
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backSlider10)
        # спрятать слайдер
        self.shortcut = QShortcut(QKeySequence("s"), self)
        self.shortcut.activated.connect(self.hideSlider)
        # показать слайдер
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_S), self)
        self.shortcut.activated.connect(self.showSlider)

        # активируем инит
        self.initui()

        # показываем всю движуху пэпси
        self.show()

    def initui(self):
        # Cоздаём видео плеер
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Кнопка Паузы
        self.playBtn = QPushButton()
        # отключаем кнопку
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # тригер
        self.playBtn.clicked.connect(self.play_video)

        # Кнопка для открытия видео
        self.oBtn = QPushButton('Open Video')
        # тригер
        self.oBtn.clicked.connect(self.open_file)

        # создаём лэйбл
        self.label = QLabel()

        # ставим слайдер вниз
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # создаём видеовиджет
        videowidget = QVideoWidget()

        # Создаём слайдер
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # создаём Шбокс
        HboxLayout = QHBoxLayout()
        HboxLayout.setContentsMargins(0, 0, 0, 0)

        # собираем виджеты в Шбокс
        HboxLayout.addWidget(self.oBtn)
        HboxLayout.addWidget(self.playBtn)
        HboxLayout.addWidget(self.slider)

        # создаём вибокс
        VboxLayout = QVBoxLayout()

        # Собираем виджеты в вибокс
        VboxLayout.addWidget(videowidget)
        VboxLayout.addLayout(HboxLayout)
        VboxLayout.addWidget(self.label)

        # Добавляем выход видео
        self.mediaPlayer.setVideoOutput(videowidget)

        self.setLayout(VboxLayout)

        # Триггеры
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        # отключаем Широкоэкранный режим
        self.widescreen = False

    # открытие файла
    def open_file(self):
        # берём имя файла
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        # проверяем, что бы название не было пустым
        if filename != '':
            # открываем файл
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        # подключаем кнопку паузы
        self.playBtn.setEnabled(True)
        # меняем иконку на Плэй
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    # Функция для паузы/воспроизведения видео
    def play_video(self):
        # проверяем стоит ли видео на паузе
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            # ставим на паузу
            self.mediaPlayer.pause()
        else:
            # воспроизводим
            self.mediaPlayer.play()

    # меняем иконку кнопки
    def mediastate_changed(self, state):
        # проверяем стоит ли пауза
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            # меняем на Паузу
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            # меняем на Плэй
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    # трэкинг позиции
    def position_changed(self, position):
        self.slider.setValue(position)

    # изменение длительности
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    # изменение позиции
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def mouseDoubleClickEvent(self, event):
        self.handleFullscreen()

    # отслеживание нажатий мыши
    def mousePressEvent(self, evt):
        self.oldPos = evt.globalPos()

    # отслеживание мыши
    def mouseMoveEvent(self, evt):
        # изменение позиции
        delta = QPoint(evt.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = evt.globalPos()

    # создаём контекстное меню
    def contextMenuRequested(self, point):
        # создаём меню
        menu = QMenu()
        # добавляем кнопки и разделители
        # открытие файла
        actionFile = menu.addAction(QIcon.fromTheme("video-x-generic"), "open File (o)")
        # разделитель
        actionclipboard = menu.addSeparator()
        # полноэкранный режим
        actionFull = menu.addAction(QIcon.fromTheme("view-fullscreen"), "Fullscreen (f)")
        # разрешение 16:9
        action169 = menu.addAction(QIcon.fromTheme("tv-symbolic"), "16 : 9")
        # разрешение 4:3
        action43 = menu.addAction(QIcon.fromTheme("tv-symbolic"), "4 : 3")
        # разделитель
        actionSep = menu.addSeparator()
        # тригерры меню
        actionFile.triggered.connect(self.open_file)
        actionFull.triggered.connect(self.handleFullscreen)
        action169.triggered.connect(self.screenpermission169)
        action43.triggered.connect(self.screenpermission43)
        menu.exec_(self.mapToGlobal(point))

    # отношение 16:9
    def screenpermission169(self):
        # входим в режим широкого экрана
        self.widescreen = True
        # берём геометрию
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        # отношение сторон
        mratio = 1.778
        # менянем разрешение
        self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))

    # отношение 4:3
    def screenpermission43(self):
        # выходим из режима широкого экрана
        self.widescreen = False
        # берём геометрию
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        # отношение сторон
        mratio = 1.33
        # менянем разрешение
        self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))

    # прячем слайдер
    def hideSlider(self):
        # прячем каждый элемент отдельно
        self.playBtn.hide()
        self.slider.hide()
        self.oBtn.hide()
        # берём геометрию окна
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        if self.widescreen:
            # устанавливаем разрешение разрешение
            self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.778))
        else:
            # устанавливаем разрешение разрешение
            self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.33))

    # меняем разрешенеие по колёсику мыши
    def wheelEvent(self, event):
        # берём переменные
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        # устанавливаем множитель, относително углу прокрутке
        mscale = event.angleDelta().y() / 5
        if self.widescreen:
            # меняем разрешение
            self.setGeometry(mleft, mtop, mwidth + mscale, round((mwidth + mscale) / 1.778))
        else:
            # меняем разрешение
            self.setGeometry(mleft, mtop, mwidth + mscale, round((mwidth + mscale) / 1.33))

    # показать слайдер и кнопки
    def showSlider(self):
        # показываем все элементы
        self.playBtn.show()
        self.slider.show()
        self.oBtn.show()
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        # проверка на полный экран
        if self.widescreen:
            # устанавливаем разрешение
            self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.55))
        else:
            # устанавливаем разрешение
            self.setGeometry(mleft, mtop, mwidth, round(mwidth / 1.33))

    # Выход/Вход в полноэкранный режим
    def handleFullscreen(self):
        # проверяем в полноэкранном режиме ли мы
        if self.windowState() & Qt.WindowFullScreen:
            # делаем курсор видимым
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            # устанавливаем обычное разрешение
            self.showNormal()
            # выводим информацию на лэйбл
            self.label.setText("no Fullscreen")
        else:
            # устанавливаем полноэкранном режим
            self.showFullScreen()
            # убираем курсор
            QApplication.setOverrideCursor(Qt.BlankCursor)
            # выводим информацию на лэйбл
            self.label.setText("Fullscreen entered")

    # вперёд на 10 минут
    def forwardSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000 * 60)

    # вперёд на 10 минут
    def forwardSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000 * 60)

    # назад на минуту
    def backSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000 * 60)

    # Назад на 10 мин
    def backSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000 * 60)

    # Повышение громкости
    def volumeUp(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
        self.label.setText("Volume: " + str(self.mediaPlayer.volume()))

    # снижение громкости
    def volumeDown(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)
        self.label.setText("Volume: " + str(self.mediaPlayer.volume()))

    # Вывод ошибок на лэйбл
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoPlayer()
    ex.setContextMenuPolicy(Qt.CustomContextMenu)
    ex.customContextMenuRequested[QPoint].connect(ex.contextMenuRequested)
    # прячем слайдер и кнопки
    ex.hideSlider()
    # ставим текст лэйбла
    ex.label.setText("Press 'o' to open file, RMB to more info")
    ex.show()
    sys.exit(app.exec())
