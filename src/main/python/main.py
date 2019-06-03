import sys

from fbs_runtime.application_context import ApplicationContext
from PyQt5 import QtWidgets, QtGui

from app import App

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    app = QtWidgets.QApplication(sys.argv)
    # load from fbs resources
    splash_image = appctxt.get_resource('signalum.png')
    pixmap = QtGui.QPixmap(splash_image)
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()
    app.setOrganizationName("BisonCorps")
    app.setApplicationName("Signalum")
    a = App()
    splash.showMessage("Loading application")
    a.setWindowTitle("Signalum Desktop - (BisonCorps, 2019)")
    a.show()
    splash.showMessage("Finished loading application")
    splash.finish(a)
    # app.exec_()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
