""" A collection of functions and classes to be used by python UI files """
import sys
import functools

import datetime as dt
import numpy as np
from scipy.interpolate import interp1d
from PyQt5 import QtWidgets


import matplotlib.figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from signalum.core import _bluetooth as bt
from signalum.core import _wifi as wf
from signalum.core._exceptions import AdapterUnaccessibleError


def calltracker(func):

    @functools.wraps(func)

    def wrapper(*args):

        wrapper.has_been_called = True
        
        return func(*args)

    wrapper.has_been_called = False

    return wrapper

# calltracker implicity tracks function call
@calltracker
def exit_error_msg(parent, title, message):
    """ A customization of QtMessageBox to exit the application after display """
    # turn off updatability while showing message to prevent repaint
    msgBox = QtWidgets.QMessageBox()
    msgBox.setText(message)
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
    key = msgBox.exec_()
    # if key == QtWidgets.QMessageBox.Ok:
        # resume updatability
        



def get_bluetooth_devices(parent, **kwargs):
    """
    Connects to the signalum library to return bluetooth table
    """
    kwargs['show_graph'] = False
    kwargs['show_name'] = True 
    kwargs['show_extra_info'] = True
    kwargs['analyze_all'] = True
    kwargs['graph'] = False
    kwargs['color'] = False
    try:
        bt_devices = bt.bluelyze(**kwargs)
    except AdapterUnaccessibleError:
        print("In exception")
        exit_error_msg(parent, "Bluetooth Adapter Unaccessible",
                    "Bluetooth thread permanently disabled, restart application with enabled adapter")
        parent.get_bt_thread.sleep()
    else:
        return bt_devices

def get_wifi_devices(**kwargs):
    """
    Connects to the signalum library to return wifi table
    """
    kwargs['show_graph'] = False
    kwargs['show_extra_info'] = True
    kwargs['analyze_all'] = True
    kwargs['graph'] = False
    kwargs['color'] = False
    wf_devices = wf.wifilyze(**kwargs)
    return wf_devices

class Graphing:
    """ Coordinate details of matplotlib graphing """
    def __init__(self, protocol):
        # TODO: create a ui to import the graph toolboxes
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.dynamic_ax = self.canvas.figure.subplots()
        # TODO: limit y axis to (-100, 0)
        # self.dynamic_ax.ylim = (-100, 0)
        # TODO: remove x ticks, let axis be clean
        # self.dynamic_ax.xticks = []
        # TODO: title axis and ylabel based on protocol
        if protocol == "bt":
            # self.dynamic_ax.title = "Bluetooth Signal Strength against time"
            # self.dynamic_ax.ylabel = "BT RSSI"
            pass
        elif protocol == "wf":
            # self.dynamic_ax.title = "Wifi Signal Strength against time"
            # self.dynamic_ax.ylabel = "WF RSSI"
            pass
        # TODO: label x-axis as time
        # self.dynamic_ax.xlabel = "Time"
        # TODO: allow setting of graph color
        # self.dynamic_ax.set_facecolor('xkcd:sky blue')
        self.signal_data = dict()
        # continous time axis
        self.x_axis = list()
        self.name_data = dict()
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
            # TODO: legend does not display, solve issue
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
