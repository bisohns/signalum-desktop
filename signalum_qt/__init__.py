""" Main Application windows """
import os
import sys
import time
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

from .qt import disabled_widget, signalum_desktop
from .threads import getDevicesDataThread
from .utils import (BluetoothProtocol, Graphing, WifiProtocol,
                    get_bluetooth_devices, get_wifi_devices)
from .widgets import ProtocolMessageWidget


class App(QtWidgets.QMainWindow, signalum_desktop.Ui_MainWindow):
    """ The main Qt Application """

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.setupUi(self)

        # Configure Application Settings
        settings = QtCore.QSettings('BisonCorps', 'signalum')
        _show_bt_services = settings.value('bt_services', False, bool)
        _show_bt_names = settings.value('bt_names', True, bool)
        _bt_refresh_rate = settings.value('bt_ref_rate', 1000, int)
        _wifi_refresh_rate = settings.value('wifi_ref_rate', 1000, int)
        _bt = settings.value('bt', False, bool)
        _wifi = settings.value('wifi', True, bool)

        # Configure Protocols
        # Bluetooth
        self.bt_graph_handler = self.configure_protocol(self.bluetoothGraphLayout,
                                                        self.bluetoothGraphToolbar, BluetoothProtocol, _bt)
        # Wifi
        self.wf_graph_handler = self.configure_protocol(self.wifiGraphLayout,
                                                        self.wifiGraphToolbar, WifiProtocol, _wifi)
        self.load_displays(_wifi, _bt)

    def configure_protocol(self, graph_layout, graph_toolbar, protocol, enabled=False):
        """ Configures a protocol for display if it has being enabled in settings """
        if enabled:
            graph_handler = Graphing(self, protocol=protocol)
            graph_layout.addWidget(graph_handler.canvas)
            graph_toolbar.addWidget(graph_handler.toolbar)
            return graph_handler
        msg_widget = ProtocolMessageWidget(self, protocol)
        graph_layout.addWidget(msg_widget)
        return None

    def load_displays(self, wifi, bluetooth):
        """ Load the wifi and bluetooth displays to the Application """
        # pass main application as parent to the fn
        # Execute only if wifi is enabled
        if wifi:
            self.get_wf_thread = getDevicesDataThread(
                lambda: get_wifi_devices(self))
            # use functools to create partial functions to run on two different threads
            wf_table_partial = partial(self.update_table, self.wifiTable)
            wf_graph_partial = partial(self.update_graph, "wf")

            # connect partial functions to their relevant signals expecting data
            self.get_wf_thread.sig.connect(wf_graph_partial)
            self.get_wf_thread.sig.connect(wf_table_partial)
            # start threads
            self.get_wf_thread.start()

        if bluetooth:
            self.get_bt_thread = getDevicesDataThread(
                lambda: get_bluetooth_devices(self))
            bt_table_partial = partial(self.update_table, self.bluetoothTable)
            bt_graph_partial = partial(self.update_graph, "bt")

            self.get_bt_thread.sig.connect(bt_graph_partial)
            self.get_bt_thread.sig.connect(bt_table_partial)

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
