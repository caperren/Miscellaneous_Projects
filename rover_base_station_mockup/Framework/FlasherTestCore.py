from PyQt5 import QtWidgets, QtCore, QtGui
import time


class Flasher(QtCore.QThread):
    THREAD_DELAY = 100
    FLASH_PERIOD = 1  # Per Second

    update_label_status__signal = QtCore.pyqtSignal()

    def __init__(self, label_gui_element, subject_text, good_text, warning_text, bad_text):
        super(Flasher, self).__init__()

        self.subject_text = subject_text

        self.label = label_gui_element  # type: QtWidgets.QLabel

        self.not_abort = True

        self.statuses = {
            "GOOD": {
                "style": "background-color: green;",
                "text": good_text
            },
            "WARNING": {
                "style": "background-color: yellow;",
                "text": warning_text
            },
            "BAD": {
                "style": "background-color: red;",
                "text": bad_text
            },
            "NEUTRAL": {
                "style": ""
            },
            "UNKNOWN": {
                "style": "background-color: black;",
                "text": "STATUS UNKNOWN"
            }
        }

        self.label_status = "BAD"

        self.current_label_status = self.label_status
        self.last_label_status = self.current_label_status

        self.connect_signals_to_slots()

        self.last_time = time.time()

    def run(self):
        while self.not_abort:
            if (time.time() - self.last_time) >= self.FLASH_PERIOD:
                if self.current_label_status in ["BAD", "WARNING", "UNKNOWN"]:
                    self.current_label_status = "NEUTRAL"
                elif self.current_label_status == "NEUTRAL":
                    self.current_label_status = self.label_status

                self.update_label_status__signal.emit()
                self.last_time = time.time()

            self.msleep(self.THREAD_DELAY)

    def connect_signals_to_slots(self):
        self.update_label_status__signal.connect(self.set_style__slot)

    def set_label_status__slot(self, status):
        text = self.subject_text

        if status in self.statuses:
            self.label_status = status
            text += "\n" + self.statuses[self.label_status]["text"]
        else:
            self.label_status = "UNKNOWN"

        self.label.setText(text)

    def set_style__slot(self):
        self.label.setStyleSheet(self.statuses[self.current_label_status]["style"])


class FlasherTest(QtCore.QThread):
    set_style_sheets_signal = QtCore.pyqtSignal()
    start_flashers__signal = QtCore.pyqtSignal()

    def __init__(self, main_window):
        super(FlasherTest, self).__init__()

        self.main_window = main_window

        self.not_abort = True

        self.label = self.main_window.label  # type: QtWidgets.QLabel
        self.label_2 = self.main_window.label_3  # type: QtWidgets.QLabel
        self.label_3 = self.main_window.label_4  # type: QtWidgets.QLabel

        self.rover_connected_flasher = Flasher(self.label, "ROVER", "CONNECTED", "INTERMITTENT", "DISCONNECTED")
        self.controller_connected_flasher = Flasher(self.label_2, "CONTROLLER", "CONNECTED", "INTERMITTENT", "DISCONNECTED")
        self.frsky_controller_connected_flasher = Flasher(self.label_3, "FRSKY", "CONNECTED", "INTERMITTENT", "DISCONNECTED")

        self.rover_connected_flasher.set_label_status__slot("GOOD")
        self.controller_connected_flasher.set_label_status__slot("WARNING")
        self.frsky_controller_connected_flasher.set_label_status__slot("BAD")

        self.start_flashers__signal.connect(self.rover_connected_flasher.start)
        self.start_flashers__signal.connect(self.controller_connected_flasher.start)
        self.start_flashers__signal.connect(self.frsky_controller_connected_flasher.start)

        self.start_flashers__signal.emit()

        self.main_window.kill_threads_signal.connect(self.on_kill_threads__slot)

    def run(self):
        start_time = time.time()
        while self.not_abort:
            if time.time() - start_time > 1:
                self.set_style_sheets_signal.emit()
                start_time = time.time()
            self.msleep(100)

    def set_style_sheets(self):
        if not self.label_last_color:
            self.label_2.setStyleSheet("background-color: yellow;")
            self.label_last_color = "asdf"
        else:
            self.label_2.setStyleSheet("")
            self.label_last_color = ""

    def on_kill_threads__slot(self):
        self.rover_connected_flasher.terminate()
        self.not_abort = False
