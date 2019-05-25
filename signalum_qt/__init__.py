import os
import sys
import time

from functools import partial
import numpy as np
import matplotlib
import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from utils import get_bluetooth_devices, get_wifi_devices
from qt import signalum_desktop
from threads import getTableValuesThread


class CanvasHandler:
    def __init__(self):
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        self.dynamic_ax = self.canvas.figure.subplots()
        self.dynamic_ax.set_facecolor('xkcd:sky blue')

    def update_canvas(self):
        """
        Update graph of canvas
        """
        self.dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self.dynamic_ax.plot(t, np.sin(t + time.time()))
        self.dynamic_ax.figure.canvas.draw()

class App(QtWidgets.QMainWindow, signalum_desktop.Ui_MainWindow):
    """ The main Qt Application """

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.setupUi(self)
        self.bt_graph_handler = CanvasHandler()
        self.wf_graph_handler = CanvasHandler()
        self.bluetoothGraphLayout.addWidget(self.bt_graph_handler.canvas)
        self.wifiGraphLayout.addWidget(self.wf_graph_handler.canvas)
        self.load_displays()

    def load_displays(self):
        """ Load the wifi and bluetooth displays to the Application """
        self.get_bt_thread = getTableValuesThread(get_bluetooth_devices)
        self.get_wf_thread = getTableValuesThread(get_wifi_devices)

        # use functools to create partials
        bt_partial = partial(self.append_data_row, self.bluetoothTable)
        wf_partial = partial(self.append_data_row, self.wifiTable)

        self.get_wf_thread.sig.connect(wf_partial)
        self.get_bt_thread.sig.connect(bt_partial)

        #start threads
        self.get_wf_thread.start()
        self.get_bt_thread.start()
        self._timer = self.bt_graph_handler.canvas.new_timer(
            100, [(self.bt_graph_handler.update_canvas, (), {})])
        self._timer.start()

    def append_data_row(self, table, data):
        """ Appends a data row to a QTableWidget"""
        table.setRowCount(len(data))
        for n, row in enumerate(data):
            for m, cell in enumerate(row):
                _entry = QtWidgets.QTableWidgetItem(str(cell))
                table.setItem(n, m, _entry)


def _run():
    """ Run the Application"""

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("BisonCorps")
    app.setApplicationName("Signalum")
    a = App()
    a.show()
    app.exec_()
