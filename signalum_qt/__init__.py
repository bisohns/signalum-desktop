#import system files
import sys
from PyQt5 import QtCore, QtGui, QtWidgets



class App(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)



def _run():
    """ Run the Application"""

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("BisonCorps")
    app.setApplicationName("Signalum")
    a = App()
    a.show()
    app.exec_()
