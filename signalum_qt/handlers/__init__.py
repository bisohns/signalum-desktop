""" A collection of functions to be used by python UI files """

from signalum.core import _bluetooth as bt
from signalum.core import _wifi as wf


def get_bluetooth_devices(**kwargs):
    """
    Connects to the signalum library to return bluetooth table
    """
    kwargs['show_graph'] = False
    kwargs['show_name'] = True 
    kwargs['show_extra_info'] = True
    kwargs['analyze_all'] = True
    kwargs['graph'] = False
    kwargs['color'] = False
    bt_devices = bt.bluelyze(**kwargs)
    return bt_devices
