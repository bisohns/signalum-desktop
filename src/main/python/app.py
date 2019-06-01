""" Main Application windows """
import os
import sys
import time
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

import resources
from qt import disabled_widget, signalum_desktop
from threads import Worker
from utils import (BluetoothProtocol, Graphing, WifiProtocol,
                   get_bluetooth_devices, get_wifi_devices)
from widgets import ProtocolMessageWidget


class App(QtWidgets.QMainWindow, signalum_desktop.Ui_MainWindow):
    """ The main Qt Application """

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.setupUi(self)

        # Define Some Actions
        playAction = self.create_action(
            '&Play...', self.start, 'Ctrl + P', 'start', 'Start Reading')
        stopAction = self.create_action(
            '&Stop...', self.stop, 'Ctrl + B', 'stop', 'Stop Reading')

        actionToolBar = self.addToolBar('Action')
        actionToolBar.setObjectName('actionToolBar')
        self.add_actions(actionToolBar, (playAction, stopAction))

        # Configure Application Settings
        self.settings = QtCore.QSettings('BisonCorps', 'signalum')
        self._bt_enabled = False
        self._wifi_enabled = False
        # WARNING: Do not interchange the flow of the lines here-after because of data-dependency
        self.configure_application()
        self.load_initial_state()
        self.saveOptionsButtonBox.accepted.connect(self.save_new_options)

        self.wf_worker = None
        self.bt_worker = None

    def configure_application(self):
        """
        Load up the application Config and UI
        """
        # Configure Protocols
        self._bt_enabled = self.settings.value('bt', False, bool)
        self._wifi_enabled = self.settings.value('wf', False, bool)
        print(self._wifi_enabled)
        # Bluetooth
        self.bt_graph_handler = self.configure_protocol(
            self.bluetoothGraphLayout, self.bluetoothGraphToolbar, BluetoothProtocol, self._bt_enabled)
        # Wifi
        self.wf_graph_handler = self.configure_protocol(
            self.wifiGraphLayout, self.wifiGraphToolbar, WifiProtocol, self._wifi_enabled)

    def load_initial_state(self):
        """
        Load up old application options
        """
        # Load Values
        _show_bt_services = self.settings.value('bt_services', False, bool)
        _show_bt_names = self.settings.value('bt_names', True, bool)
        _bt_refresh_rate = self.settings.value('bt_ref_rate', 1, int)
        _wifi_refresh_rate = self.settings.value('wifi_ref_rate', 1, int)
        # Update UI with values
        self.wifiSwitch.setChecked(self._wifi_enabled)
        self.bluetoothSwitch.setChecked(self._bt_enabled)
        self.bluetoothRefreshRate.setValue(_bt_refresh_rate)
        self.wifiRefreshRate.setValue(_wifi_refresh_rate)
        self.showBluetoothServices.setChecked(_show_bt_services)
        self.showBluetoothNames.setChecked(_show_bt_names)

    def clear_layout(self, layout):
        """ 
        clears all the widgets and children within `layout` 
        """
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def save_new_options(self):
        """
        Saves the options to QSettings after the click of save Button
        """
        self.settings.setValue('bt', self.bluetoothSwitch.isChecked())
        self.settings.setValue('wf', self.wifiSwitch.isChecked())
        self.settings.setValue(
            'bt_ref_rate', self.bluetoothRefreshRate.value())
        self.settings.setValue('wifi_ref_rate', self.wifiRefreshRate.value())
        self.settings.setValue(
            'bt_services', self.showBluetoothServices.isChecked())
        self.settings.setValue('bt_names', self.showBluetoothNames.isChecked())
        success = QtWidgets.QMessageBox.information(
            self, 'Signalum', 'Changes Saved Successfully')
        # Reload Application UI and protocol
        self.clear_layout(self.bluetoothGraphLayout)
        self.clear_layout(self.wifiGraphLayout)
        self.clear_layout(self.bluetoothGraphToolbar)
        self.clear_layout(self.wifiGraphToolbar)
        self.configure_application()

    def create_action(self, text, slot=None, shortcut=None, icon=None, tip=None,
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

    def add_actions(self, target, actions):
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

    def start_protocol_thread(self, protocol, update_fn, table, refresh_rate):
        """
        Starts a thread for a protocol. The protocol devices are updated
        based on the `update_fn` passed as arg
        """
        thread = QtCore.QThread(self)
        worker = Worker(
            lambda: update_fn(self), '%sThreadWorker' % protocol, refresh_rate)
        worker.moveToThread(thread)
        # use functools to create partial functions to run on two different threads
        table_partial = partial(self.update_table, table)
        graph_partial = partial(self.update_graph, protocol)

        # connect partial functions to their relevant signals expecting data
        worker.sig.connect(graph_partial)
        worker.sig.connect(table_partial)
        # start threads
        thread.started.connect(worker.operate)
        worker.finished.connect(thread.quit)
        thread.start()
        return worker

    def load_displays(self, wifi, bluetooth):
        """
        Load the wifi and bluetooth displays to the Application
        """
        # pass main application as parent to the fn
        # Execute only if wifi is enabled
        if wifi:
            wifi_refresh_rate = self.settings.value('wifi_ref_rate', 1000, int)
            self.wf_worker = self.start_protocol_thread(
                WifiProtocol, get_wifi_devices, self.wifiTable, wifi_refresh_rate)
        if bluetooth:
            bt_refresh_rate = self.settings.value('bt_ref_rate', 1000, int)
            self.bt_worker = self.start_protocol_thread(
                BluetoothProtocol, get_bluetooth_devices, self.bluetoothTable, bt_refresh_rate)

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
        if protocol.is_wifi():
            self.wf_graph_handler.update_canvas(data)
        elif protocol.is_bt():
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
        if self.bt_worker:
            self.bt_worker.stop_action()
        if self.wf_worker:
            self.wf_worker.stop_action()
