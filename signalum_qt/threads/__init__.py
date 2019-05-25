""" Thread handlers for running in background """

from PyQt5 import QtGui
from PyQt5.QtCore import QThread, QObject, pyqtSignal

class getTableValuesThread(QThread, QObject):
    sig = pyqtSignal(list)

    def __init__(self, table_fn):
        """
        """
        QThread.__init__(self)
        self.table_fn = table_fn

    def __del__(self):
        self.wait()

    def run(self):
        """
        Run on an individual thread and emit values
        """
        while True:
            values, _ = self.table_fn() 
            print(values)
            if values:
                self.sig.emit(values)
            else:
                self.sig.emit([])
            self.sleep(1)