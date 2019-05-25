import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from qt import signalum


class App(QtWidgets.QMainWindow, signalum.Ui_MainWindow):
    """ The main Qt Application """

    def __init__(self, parent=None):
        super(App, self).__init__(parent=parent)
        self.setupUi(self)



def _run():
    """ Run the Application"""

    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("BisonCorps")
    app.setApplicationName("Signalum")
    a = App()
    a.show()
    app.exec_()
