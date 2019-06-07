""" Thread handlers for running in background """

from PyQt5 import QtGui
from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal, pyqtSlot
from signalum.core._exceptions import AdapterUnaccessibleError

from utils import exit_error_msg


class Worker(QObject):
    """
    Thread Worker to run a retrieve devices function independently

    Args:
        table_fn(function): function to retrieve device data at single instance
    """

    sig = pyqtSignal(list)
    finished = pyqtSignal()

    def __init__(self, table_fn, object_name, refresh_rate, protocol):
        """
        """
        super(Worker, self).__init__()
        self.table_fn = table_fn
        self.setObjectName(object_name)
        self._continue = True
        self.refresh_rate = refresh_rate
        self.protocol = protocol

    @pyqtSlot()
    def operate(self):
        """
        Infinite function to get devices list from `table_fn` and emit the signal containing list
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_update)
        self.timer.start(self.refresh_rate * 1000)

    def get_update(self):
        if not self._continue:
            self.timer.stop()
            self.finished.emit()
        else:
            # For cases where the adapter is off. No readings are return
            try:
                values, _ = self.table_fn.__call__()
            except AdapterUnaccessibleError:
                exit_error_msg(None, f"{self.protocol} Adapter Unaccessible",
                               f"Enable your {self.protocol} adapter and restart sensing."
                               f"You can deactivate the {self.protocol} sensing in your settings"
                               "if adapter is not available")
                self._continue = False
            except (ValueError, TypeError):
                pass
            else:
                if not values:
                    values = []
                print(values)
                self.sig.emit(values)

    def stop_action(self):
        self._continue = False
