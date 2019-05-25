import os
import sys

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from .handlers import get_bluetooth_devices
from .qt import signalum_desktop


class App(QtWidgets.QMainWindow, signalum_desktop.Ui_MainWindow):
    """ The main Qt Application """

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.setupUi(self)
        self.load_displays()

    def load_displays(self):
        """ Load the wifi and bluetooth displays to the Application """
        self.add_bluelyze()

    def add_bluelyze(self):
        """ Get the bluetooth devices for plotting and listing """
        bluetooth_devices, _ = get_bluetooth_devices()
        self.append_data_row(self.bluetoothTable, bluetooth_devices)

    def add_wifilyze(self):
        """ Get the wifi devices for plotting and listing """
        pass

    def append_data_row(self, table, data):
        """ Appends a data row to a QTableWidget"""
        table.setRowCount(len(data))
        for n, row in enumerate(data):
            for m, cell in enumerate(row):
                _entry = QtWidgets.QTableWidgetItem(cell)
                table.setItem(m, n, _entry)


def _run():
    """ Run the Application"""

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("BisonCorps")
    app.setApplicationName("Signalum")
    a = App()
    a.show()
    app.exec_()
