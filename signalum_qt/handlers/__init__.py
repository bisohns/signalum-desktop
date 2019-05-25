""" A collection of functions to be used by python UI files """
# get needful 
from signalum.core import _bluetooth as bt
from signalum.core import _wifi as wf

def get_bluetooth_devices(**kwargs):
    """
    Connects to the signalum library to return bluetooth table
    """
    kwargs['analyze_all'] = True
    kwargs['graph'] = False
    bt_devices = bt.bluelyze(**kwargs)
    return bt_devices