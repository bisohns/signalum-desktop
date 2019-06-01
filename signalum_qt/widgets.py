""" Custom Widgets """

from PyQt5 import QtCore, QtGui, QtWidgets

from .qt import disabled_widget


class ProtocolMessageWidget(QtWidgets.QWidget, disabled_widget.Ui_Form):
    """ Displays message notifications for protocol """

    def __init__(self, parent=None, protocol='Bluetooth', custom_header="", custom_msg=""):
        super(ProtocolMessageWidget, self).__init__(parent=parent)
        self.setupUi(self)
        if not custom_header:
            self.MessageLabel.setText(str(protocol) + ' Mode is Disabled')
        else:
            self.MessageLabel.setText(custom_header)
            self.MessageBodyLabel.setText(custom_msg)
