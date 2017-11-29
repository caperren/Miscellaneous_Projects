#!/usr/bin/env python

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
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import signal
import ctypes
import logging
import time

# Custom Imports
from Framework.FlasherTestCore import FlasherTest
from Framework.VideoCore import Video
# from Framework.SettingsCore import Settings
# from Framework.LoggingCore import Logger
# from Interface.InterfaceCore import Interface
# from Framework.GameControllerCore import GameController
# from Framework.RoverControllerCore import RoverController

#####################################
# Global Variables
#####################################
UI_FILE_PATH = "Resources/UI/RoverGui.ui"


#####################################
# Application Class Definition
#####################################
class ApplicationWindow(QtWidgets.QMainWindow):
    kill_threads_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        # noinspection PyArgumentList
        super(ApplicationWindow, self).__init__(parent)
        uic.loadUi(UI_FILE_PATH, self)

        # ########## Class Variables ##########
        self.num_threads_running = 0
        self.threads = []

        self.primary_display_label = self.primary_display_label  # type: QtWidgets.QLabel
        self.secondary_display_label = self.secondary_display_label  # type: QtWidgets.QLabel
        self.tertiary_display_label = self.tertiary_display_label  # type: QtWidgets.QLabel

        # self.primary_display_label.setPixmap(QtGui.QPixmap("Resources/Images/steller_at_terminus.png").scaledToHeight(1080))
        # self.secondary_display_label.setPixmap(QtGui.QPixmap("Resources/Images/mountain_closeup.jpg"))
        # self.tertiary_display_label.setPixmap(QtGui.QPixmap("Resources/Images/mountains_from_marys_peak.jpg"))

        self.flasher = FlasherTest(self)
        self.video = Video(self)

        self.threads.append(self.flasher)
        self.threads.append(self.video)
        # self.gps_lock_button = self.gps_lock_button  # type: QtWidgets.QPushButton
        # self.gps_lock_button.setCheckable(True)

        # ########## Instantiation of program classes ##########
        # Settings class and version number set
        # self.settings_class = Settings(self)
        # self.settings = QtCore.QSettings()
        # self.settings.setValue("miscellaneous/version", __version__)

        # Uncomment these lines to completely reset settings and quit, then re-comment and rerun program
        # self.settings.clear()
        # self.close()

        # Set up the global logger instance
        # self.logger_class = Logger(console_output=True)
        # self.logger = logging.getLogger("RoverBaseStation")
        #
        # # All interface elements
        # self.controller_class = GameController(self)
        # self.interface_class = Interface(self)
        # self.rover_controller_class = RoverController(self)
        #
        # # ########## Add threads to list for easy access on program close ##########
        # self.threads.append(self.interface_class.live_logs_class)
        # self.threads.append(self.controller_class)
        # self.threads.append(self.rover_controller_class)

        # ########## Set up QT Application Window ##########
        self.show()

    def closeEvent(self, event):
        # Tell all threads to die
        self.kill_threads_signal.emit()

        # Wait for all the threads to end properly
        for thread in self.threads:
            thread.wait()

        # Print final log noting shutdown and shutdown the logger to flush to disk
        # self.logger.debug("########## Application Stopping ##########")
        logging.shutdown()

        # Accept the close event to properly close the program
        event.accept()


#####################################
# Main Definition
#####################################
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)            # This allows the keyboard interrupt kill to work  properly
    application = QtWidgets.QApplication(sys.argv)          # Create the base qt gui application
    app_window = ApplicationWindow()                        # Make a window in this application
    app_window.setWindowTitle("Rover Base Station")         # Sets the window title

    # app_window.setFixedSize(1920, 1080)
    app_window.showFullScreen()
    app_window.show()                                           # Show the window in the application
    application.exec_()                                         # Execute launching of the application
