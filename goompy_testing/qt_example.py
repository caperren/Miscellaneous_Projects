#!/usr/bin python3.5

"""
    Main file used to launch the Rover Base Station
    No other files should be used for launching this application.
"""

__author__ = "Corwin Perren"
__credits__ = [""]
__license__ = "GPL (GNU General Public License) 3.0"
__version__ = "0.1"
__maintainer__ = "Corwin Perren"
__email__ = "caperren@caperren.com"
__status__ = "Development"

#####################################
# Imports
#####################################
# Python native imports
import sys
from PyQt5 import QtWidgets, QtCore, QtGui, uic, QtWebEngine, QtQuick, QtQml
import signal
import logging
import time
from goompy import GooMPy
from PIL.ImageQt import ImageQt
import PIL

#####################################
# Global Variables
#####################################
UI_FILE_PATH = "ui.ui"


LATITUDE = 38.4064262
LONGITUDE = -110.794115
ZOOM = 18  # 15,16, and 18 18 seems best
MAPTYPE = 'satellite'

WIDTH = 640
HEIGHT = 640


#####################################
# Application Class Definition
#####################################
class ApplicationWindow(QtWidgets.QMainWindow):
    connect_all_signals_to_slots_signal = QtCore.pyqtSignal()
    start_all_threads = QtCore.pyqtSignal()
    kill_threads_signal = QtCore.pyqtSignal()

    image_shown_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(ApplicationWindow, self).__init__(parent)
        uic.loadUi(UI_FILE_PATH, self)

        # ########## Class Variables ##########
        self.num_threads_running = 0
        self.threads = []  # type: [QtCore.QThread]

        # ########## Instantiation of program classes ##########
        # Settings class and version number set

        # Uncomment these lines to completely reset settings and quit, then re-comment and rerun program
        # self.settings.clear()
        # self.close()

        self.label = self.label  # type: QtWidgets.QLabel

        self.read_updater = ReadUpdater(self)

        # ########## Add threads to list for easy access on program close ##########
        self.threads.append(self.read_updater)

        # ########## Setup signal/slot connections ##########
        for thread in self.threads:
            self.connect_all_signals_to_slots_signal.connect(thread.connect_signals_to_slots__slot)

        self.connect_all_signals_to_slots_signal.emit()

        # ########## Start all child threads ##########
        for thread in self.threads:
            self.start_all_threads.connect(thread.start)

        self.start_all_threads.emit()

        time.sleep(1)

        # ########## Ensure all threads started properly ##########
        for thread in self.threads:
            if not thread.isRunning():
                self.logger.error("Thread" + thread.__class__.__name__ + " failed to start! Exiting...")
                for thread in self.threads:
                    thread.terminate()
                self.close()

        # self.logger.info("All threads started successfully!")

    def show_graphics_view__slot(self):
        self.graphicsView.show()
        self.label.setPixmap(self.read_updater.pix)


    def closeEvent(self, event):
        # Tell all threads to die
        self.kill_threads_signal.emit()

        # Wait for all the threads to end properly
        for thread in self.threads:
            thread.wait()

        # Print final log noting shutdown and shutdown the logger to flush to disk
        self.logger.debug("########## Application Stopping ##########")
        logging.shutdown()

        # Accept the close event to properly close the program
        event.accept()


class ReadUpdater(QtCore.QThread):

    request_viewport_update = QtCore.pyqtSignal()

    def __init__(self, main_window):
        super(ReadUpdater, self).__init__()

        # ########## Reference to top level window ##########
        self.main_window = main_window  # type: QtWidgets.QMainWindow

        # ########## Get the settings instance ##########
        self.settings = QtCore.QSettings()

        # ########## Get the Pick And Plate instance of the logger ##########
        self.logger = logging.getLogger("RoverBaseStation")

        self.goompy = GooMPy(2*WIDTH, HEIGHT, LATITUDE, LONGITUDE, ZOOM, MAPTYPE, 1500)

        self.tab_widget = self.main_window.tabWidget  # type: QtWidgets.QTabWidget

        # ########## Some Flags ##########
        self.run_thread_flag = True

        # ########## Class variables ##########
        self.data_last_seen = time.time()

    def run(self):
        #self.logger.debug("Read Updater Thread Starting...")

        self.request_viewport_update.connect(self.main_window.show_graphics_view__slot)
        #self.goompy.move(650, 400)

        dx = 1
        dy = 1

        x_num = 0
        y_num = 0

        dir_x = 0
        dir_y = 0

        count_max = 500

        while self.run_thread_flag:

            #self.scene.clear()

            #self.scene = QtWidgets.QGraphicsScene(self)
            #self.graphics_view.setScene(self.scene)
            if dir_x:
                self.goompy.move(-dx, 0)
                x_num -= 1
            else:
                self.goompy.move(dx, 0)
                x_num += 1

            if dir_y:
                self.goompy.move(0, -dy)
                y_num -= 1
            else:
                self.goompy.move(0, dy)
                y_num += 1




            if x_num >= count_max:
                dir_y = 1
                dir_x = 1
            elif x_num <= 0:
                dir_y = 0
                dir_x = 0

            self.image = self.goompy.getImage().convert("RGBA")  # type: PIL.Image.Image
            print(self.goompy.northwest)
            print(self.goompy.southeast)
            print(self.goompy.uppery)
            print(self.goompy.leftx)
            print(self.goompy.bigimage.size)
            #self.goompy.

            #self.image = self.image.crop((500, 500, 750, 750))

            print(self.image)


            # print(self.image.height)
            # print(self.image.width)

            qim = ImageQt(self.image)
            #self.pix.
              # type: QtGui.QPixmap

            # print(test)
            # test.setPixmap(pixmap)

            # print(self.pix.width())
            # print(self.pix.height())
            # print(self.pix.colorCount())

            # self.pix
            self.pix = QtGui.QPixmap.fromImage(qim)
            self.request_viewport_update.emit()

            # while self.wait_til_shown:
            #     self.msleep(1)


            self.msleep(20)

        #self.logger.debug("Read Updater Thread Stopping...")



    def connect_signals_to_slots__slot(self):

        self.main_window.kill_threads_signal.connect(self.on_kill_threads__slot)

    def on_image_shown__slot(self):
        self.wait_til_shown = False

    def on_kill_threads__slot(self):
        self.run_thread_flag = False

#####################################
# Main Definition
#####################################
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # This allows the keyboard interrupt kill to work  properly
    application = QtWidgets.QApplication(sys.argv)  # Create the base qt gui application
    app_window = ApplicationWindow()  # Make a window in this application
    app_window.setWindowTitle("Rover Base Station")  # Sets the window title
    app_window.show()  # Show the window in the application
    application.exec_()  # Execute launching of the application
