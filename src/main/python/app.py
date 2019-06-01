""" Main Application windows """
import os
import sys
import time
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

import resources
from qt import disabled_widget, signalum_desktop
from threads import WorkerThread
from utils import (BluetoothProtocol, Graphing, WifiProtocol,
                   get_bluetooth_devices, get_wifi_devices)
from widgets import ProtocolMessageWidget


class App(QtWidgets.QMainWindow, signalum_desktop.Ui_MainWindow):
    """ The main Qt Application """

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.setupUi(self)

        # Define Some Actions
        playAction = self.createAction(
            '&Play...', self.start, 'Ctrl + P', 'start', 'Start Reading')

        stopAction = self.createAction(
            '&Stop...', self.stop, 'Ctrl + B', 'stop', 'Stop Reading')

        actionToolBar = self.addToolBar('Action')
        actionToolBar.setObjectName('actionToolBar')
        self.addActions(actionToolBar, (playAction, stopAction))

        # Configure Application Settings
        settings = QtCore.QSettings('BisonCorps', 'signalum')
        _show_bt_services = settings.value('bt_services', False, bool)
        _show_bt_names = settings.value('bt_names', True, bool)
        _bt_refresh_rate = settings.value('bt_ref_rate', 1000, int)
        _wifi_refresh_rate = settings.value('wifi_ref_rate', 1000, int)
        self._bt_enabled = settings.value('bt', False, bool)
        self._wifi_enabled = settings.value('wifi', True, bool)

        # Configure Protocols
        # Bluetooth
        self.bt_graph_handler = self.configure_protocol(
            self.bluetoothGraphLayout, self.bluetoothGraphToolbar, BluetoothProtocol, self._bt_enabled)
        # Wifi
        self.wf_graph_handler = self.configure_protocol(
            self.wifiGraphLayout, self.wifiGraphToolbar, WifiProtocol, self._wifi_enabled)

    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None,
                     checkable=False, signal='triggered'):
        """ Creates an Action """
        action = QtWidgets.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(':/%s.png' % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        """ Add action to a toolbar or menu """
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

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
        """
        Load the wifi and bluetooth displays to the Application 
        """
        # pass main application as parent to the fn
        # Execute only if wifi is enabled
        if wifi:
            self.wf_thread = WorkerThread(
                lambda: get_wifi_devices(self), 'WifiThreadWorker')
            # use functools to create partial functions to run on two different threads
            wf_table_partial = partial(self.update_table, self.wifiTable)
            wf_graph_partial = partial(self.update_graph, "wf")

            # connect partial functions to their relevant signals expecting data
            self.wf_thread.sig.connect(wf_graph_partial)
            self.wf_thread.sig.connect(wf_table_partial)
            # start threads
            self.wf_thread.start()

#         if bluetooth:
#             self.get_bt_thread = DevicesDataThread(
#                 lambda: get_bluetooth_devices(self), 'BluetoothThread')
#             bt_table_partial = partial(self.update_table, self.bluetoothTable)
#             bt_graph_partial = partial(self.update_graph, "bt")

#             self.get_bt_thread.sig.connect(bt_graph_partial)
#             self.get_bt_thread.sig.connect(bt_table_partial)

#             self.get_bt_thread.start()

    def update_table(self, table, data):
        """ 
        Appends a data row to a QTableWidget
        """
        # Update Table Data
        table.setRowCount(len(data))
        for n, row in enumerate(data):
            for m, cell in enumerate(row):
                _entry = QtWidgets.QTableWidgetItem(str(cell))
                table.setItem(n, m, _entry)

    def update_graph(self, protocol, data):
        """ 
        Update graph 
        """
        # self.bt_graph_handler.update_canvas(data)
        if protocol == "wf":
            self.wf_graph_handler.update_canvas(data)
        elif protocol == "bt":
            self.bt_graph_handler.update_canvas(data)

    def start(self):
        """ 
        Starts reading the signalum application 
        """
        self.load_displays(self._wifi_enabled, self._bt_enabled)

    def stop(self):
        """ 
        Stops the signalum process. This terminates the running threads 
        """
#         self.get_bt_thread.stop_action()
        self.wf_thread_worker.stop_action()
