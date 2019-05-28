""" Thread handlers for running in background """

from PyQt5 import QtGui
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from signalum.core._exceptions import AdapterUnaccessibleError

from .utils import exit_error_msg

class getDevicesDataThread(QThread, QObject):
    """
    Thread to run a retrieve devices function independently

    Args:
        table_fn(function): function to retrieve device data at single instance
    """
    sig = pyqtSignal(list)

    def __init__(self, table_fn):
        """
        """
        QThread.__init__(self)
        self.table_fn = table_fn

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def run(self):
        """
        Infinite function to get devices list from `table_fn` and emit the signal containing list
        """
        while True:
            # For cases where the adapter is off. No readings are return
            try:
                values, _ = self.table_fn.__call__() 
            except (ValueError, TypeError):
                pass
            else:
                if not values:
                    values = []
                print(exit_error_msg.has_been_called)
                print(values)
                self.sig.emit(values)


