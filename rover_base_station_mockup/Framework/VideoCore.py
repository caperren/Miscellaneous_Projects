from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimediaWidgets
import time
import cv2
import qimage2ndarray
import PIL.Image
from PIL.ImageQt import ImageQt

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5


class Compass(QtCore.QThread):
    compass_ready__signal = QtCore.pyqtSignal()

    def __init__(self, main_window):
        super(Compass, self).__init__()

        self.main_window = main_window

        self.not_abort = True

        self.image = PIL.Image.open("Resources/Images/compass.png").resize((300, 300))  # PIL.Image
        self.compass_dir = 1

        self.compass_label = self.main_window.compass_label  # type: QtWidgets.QLabel
        self.compass_frame = None
        self.compass_current_degrees_rotation = 0

        self.main_window.kill_threads_signal.connect(self.on_kill_threads__slot)
        self.compass_ready__signal.connect(self.on_compass_ready__slot)

        self.start()

    def run(self):
        while self.not_abort:
            new = self.image.rotate(int(self.compass_current_degrees_rotation))

            if self.compass_current_degrees_rotation == 90:
                self.compass_dir = 0
            elif self.compass_current_degrees_rotation == -90:
                self.compass_dir = 1

            if self.compass_dir:
                self.compass_current_degrees_rotation += 1
            else:
                self.compass_current_degrees_rotation -= 1

            self.compass_frame = QtGui.QPixmap.fromImage(ImageQt(new))
            self.compass_ready__signal.emit()

            self.msleep(50)

    def on_compass_ready__slot(self):
        self.compass_label.setPixmap(self.compass_frame)

    def on_kill_threads__slot(self):
        self.not_abort = False


class VideoReader(QtCore.QThread):
    video_frame_ready__signal = QtCore.pyqtSignal()

    def __init__(self, main_window):
        super(VideoReader, self).__init__()

        self.main_window = main_window

        self.not_abort = True

        self.primary_display_label = self.main_window.primary_display_label  # type: QtWidgets.QLabel

        self.main_window.kill_threads_signal.connect(self.on_kill_threads__slot)
        self.video_frame_ready__signal.connect(self.on_compass_ready__slot)

        # self.video = cv2.imread("Resources/Videos/ROSS1.MOV")

        self.video_frame = None

        self.start()

    def run(self):
        while self.not_abort:
            frame = self.video_camera.read()[1]

            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # frame = cv2.resize(frame, (1280, 720))
            # self.video_frame = QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(frame))

            self.video_frame_ready__signal.emit()

            self.msleep(50)

    def on_compass_ready__slot(self):
        self.primary_display_label.setPixmap(self.video_frame)

    def on_kill_threads__slot(self):
        self.not_abort = False


class Video(QtCore.QThread):
    image_ready_signal = QtCore.pyqtSignal()

    def __init__(self, main_window):
        super(Video, self).__init__()

        self.main_window = main_window

        self.not_abort = True

        self.primary_display_label = self.main_window.primary_display_label  # type: QtWidgets.QLabel
        self.secondary_display_label = self.main_window.secondary_display_label  # type: QtWidgets.QLabel
        self.tertiary_display_label = self.main_window.tertiary_display_label  # type: QtWidgets.QLabel

        self.video_camera = cv2.VideoCapture(0)

        self.video_camera.set(CV_CAP_PROP_FRAME_WIDTH, 1280)
        self.video_camera.set(CV_CAP_PROP_FRAME_HEIGHT, 720)
        self.video_camera.set(CV_CAP_PROP_FPS, 15)

        self.main_window.kill_threads_signal.connect(self.on_kill_threads__slot)
        self.image_ready_signal.connect(self.on_image_ready__slot)

        self.raw_frame = None
        self.large_frame = None
        self.small_frame = None

        self.compass = Compass(self.main_window)
        # self.video_reader = VideoReader(self.main_window)

        self.start()

    def run(self):
        frame_count = 0
        start_time = time.time()

        while self.not_abort:
            frame = self.video_camera.read()[1]

            self.raw_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.large_frame = self.raw_frame
            self.small_frame = cv2.resize(self.raw_frame, (640, 360))
            self.large_frame = QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(self.large_frame))
            self.small_frame = QtGui.QPixmap.fromImage(qimage2ndarray.array2qimage(self.small_frame))

            self.image_ready_signal.emit()

            frame_count += 1
            fps = frame_count / (time.time() - start_time)
            # print("FPS:", fps)

            self.msleep(1)

        self.compass.wait()
        #self.video_reader.wait()

    def on_image_ready__slot(self):
        pass
        self.primary_display_label.setPixmap(self.large_frame)
        self.secondary_display_label.setPixmap(self.small_frame)
        self.tertiary_display_label.setPixmap(self.small_frame)

    def on_kill_threads__slot(self):
        self.not_abort = False
