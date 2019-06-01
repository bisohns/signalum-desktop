import sys

from fbs_runtime.application_context import ApplicationContext
from PyQt5 import QtWidgets

from app import App

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName("BisonCorps")
    app.setApplicationName("Signalum")
    a = App()
    a.show()
    app.exec_()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
