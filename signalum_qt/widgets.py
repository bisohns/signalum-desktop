""" Custom Widgets """

from PyQt5 import QtCore, QtGui, QtWidgets

from .qt import disabled_widget


class ProtocolDisabledWidget(QtWidgets.QWidget, disabled_widget.Ui_Form):
    """ Displays message notifications when a protocol is not enabled """

    def __init__(self, parent=None, protocol='Bluetooth'):
        super(ProtocolDisabledWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.MessageLabel.setText(str(protocol) + ' Mode is Disabled')
