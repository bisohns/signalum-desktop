import os
import sys

from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from utils import get_bluetooth_devices, get_wifi_devices, Graphing
from qt import signalum_desktop
from threads import getTableValuesThread


class App(QtWidgets.QMainWindow, signalum_desktop.Ui_MainWindow):
    """ The main Qt Application """

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.setupUi(self)
        self.bt_graph_handler = Graphing(protocol="bt")
        self.wf_graph_handler = Graphing(protocol="wf")
        self.bluetoothGraphLayout.addWidget(self.bt_graph_handler.canvas)
        self.wifiGraphLayout.addWidget(self.wf_graph_handler.canvas)
        self.load_displays()

    def load_displays(self):
        """ Load the wifi and bluetooth displays to the Application """
        self.get_bt_thread = getTableValuesThread(get_bluetooth_devices)
        self.get_wf_thread = getTableValuesThread(get_wifi_devices)

        # use functools to create partials
        bt_partial = partial(self.update_table_graph, self.bluetoothTable, "bt")
        wf_partial = partial(self.update_table_graph, self.wifiTable, "wf")

        self.get_wf_thread.sig.connect(wf_partial)
        self.get_bt_thread.sig.connect(bt_partial)

        #start threads
        self.get_wf_thread.start()
        self.get_bt_thread.start()

    def update_table_graph(self, table, protocol, data):
        """ Appends a data row to a QTableWidget"""
        # Update Table Data
        table.setRowCount(len(data))
        for n, row in enumerate(data):
            for m, cell in enumerate(row):
                _entry = QtWidgets.QTableWidgetItem(str(cell))
                table.setItem(n, m, _entry)
        # Update Graph Data
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
