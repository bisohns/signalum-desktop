import os
import sys

from functools import partial
import numpy as np
import datetime as dt
from scipy.interpolate import interp1d
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
    def __init__(self, protocol):
        self.fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.fig)
        self.dynamic_ax = self.canvas.figure.subplots()
        # limit the axis to 100
        # self.dynamic_ax.ylim = (-100, 0)
        # remove x ticks
        # self.dynamic_ax.xticks = []
        if protocol == "bt":
            # self.dynamic_ax.title = "Bluetooth Signal Strength against time"
            # self.dynamic_ax.ylabel = "BT RSSI"
            pass
        elif protocol == "wf":
            # self.dynamic_ax.title = "Wifi Signal Strength against time"
            # self.dynamic_ax.ylabel = "WF RSSI"
            pass
        # x axis label is time
        # self.dynamic_ax.xlabel = "Time"
        # self.dynamic_ax.set_facecolor('xkcd:sky blue')
        self.signal_data = {}
        # continous time axis
        self.x_axis = []
        self.name_data = {}
        # number of values to always have in a graph
        self.limit = -30
        # impossibly low value to indicate out of range
        self.out_of_range = -200

    def update_canvas(self, data):
        """
        Update graph of canvas
        """
        self.update_data(data)
        self.dynamic_ax.clear()
        # turn time data to numpy array
        # limit x axis
        self.x_axis = self.x_axis[self.limit:]
        xs = np.array(self.x_axis)
        x_new = np.linspace(xs.min(), xs.max(), 500)
        for i, j in zip(self.signal_data.values(), self.signal_data.keys()):
            # get device name from name dictionary
            device_name = self.name_data[j]
            print(device_name)    
            # list of rssi values will be plotted on the y axis
            y = np.array(i)
            y = y[self.limit:]
            # check if points are enough to interpolate on
            if len(i) > 2:
                f = interp1d(xs, y, kind='nearest')
                y_smooth = f(x_new)
                # plot smooth plot with scatter point plots
                self.dynamic_ax.plot(x_new, y_smooth, label=device_name)
                self.dynamic_ax.figure.canvas.draw()
            else:
                self.dynamic_ax.plot(xs, y, label=device_name)
                self.dynamic_ax.figure.canvas.draw()
        self.dynamic_ax.legend()
    
    def update_data(self, data):
        """ Update the data for display """
        # TODO Update the data accordingly
        # self.data[address] = 
        macs = [i[1] for i in data]
        names = [i[0] for i in data]
        rssi = [i[2] for i in data]
        # set x data (real time)
        self.x_axis.append(float(dt.datetime.now().strftime("%H.%M%S")))
        # limit x axis to the predefined limit
        for a, (x, y) in enumerate(zip(macs, rssi)):
            try:
                assert self.signal_data[x]
            except KeyError:
                # if device history was not found, create one with out of range values
                self.signal_data[x] = [self.out_of_range for i in range(len(self.x_axis) - 1)]
            finally:
                # add device name to name dictionary
                self.name_data[x] = str(names[a])   
                # append signal data to signal dictionary 
                self.signal_data[x].append(y)
        key_list = [i for i in self.signal_data.keys()]
        # find devices that were not discovered but were discovered before
        no_val = np.setdiff1d(key_list, macs)
        # append out of range values to those devices
        for i in no_val:
            self.signal_data[i].append(self.out_of_range)
            

class App(QtWidgets.QMainWindow, signalum_desktop.Ui_MainWindow):
    """ The main Qt Application """

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.setupUi(self)
        self.bt_graph_handler = CanvasHandler(protocol="bt")
        self.wf_graph_handler = CanvasHandler(protocol="wf")
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
