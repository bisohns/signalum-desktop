import os
import sys
import time

from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from .utils import get_bluetooth_devices, get_wifi_devices, Graphing
from .qt import signalum_desktop
from .threads import getDevicesDataThread

class App(QtWidgets.QMainWindow, signalum_desktop.Ui_MainWindow):
    """ The main Qt Application """

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.setupUi(self)

        self.bt_graph_handler = Graphing(protocol="bt")
        self.wf_graph_handler = Graphing(protocol="wf")
        # Checks that detect wifi and bluetooth adapter availability
        self.bluetooth_enabled = False
        self.wifi_enabled = False
        # add graph handler canvas to their relevant layouts
        self.bluetoothGraphLayout.addWidget(self.bt_graph_handler.canvas)
        self.wifiGraphLayout.addWidget(self.wf_graph_handler.canvas)
        self.load_displays()

    def load_displays(self):
        """ Load the wifi and bluetooth displays to the Application """
        self.get_bt_thread = getDevicesDataThread(lambda : get_bluetooth_devices(self))
        self.get_wf_thread = getDevicesDataThread(get_wifi_devices)

        # use functools to create partial functions to run on two different threads
        bt_table_partial = partial(self.update_table, self.bluetoothTable)
        wf_table_partial = partial(self.update_table, self.wifiTable)
        bt_graph_partial = partial(self.update_graph, "bt")
        wf_graph_partial = partial(self.update_graph, "wf")


        # connect partial functions to their relevant signals expecting data
        self.get_wf_thread.sig.connect(wf_graph_partial)
        self.get_wf_thread.sig.connect(wf_table_partial)
        self.get_bt_thread.sig.connect(bt_graph_partial)
        self.get_bt_thread.sig.connect(bt_table_partial)

        #start threads
        self.get_wf_thread.start()
        self.get_bt_thread.start()

    def update_table(self, table, data):
        """ Appends a data row to a QTableWidget"""
        # Update Table Data
        table.setRowCount(len(data))
        for n, row in enumerate(data):
            for m, cell in enumerate(row):
                _entry = QtWidgets.QTableWidgetItem(str(cell))
                table.setItem(n, m, _entry)
    
    def update_graph(self, protocol, data):
        """ Update graph """
        # self.bt_graph_handler.update_canvas(data)
        if protocol == "wf":
            self.wf_graph_handler.update_canvas(data)
        elif protocol == "bt":
            self.bt_graph_handler.update_canvas(data)




def _run():
    """ Run the Application"""

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("BisonCorps")
    app.setApplicationName("Signalum")
    a = App()
    a.show()
    app.exec_()
