""" Custom Widgets """

from PyQt5 import QtCore, QtGui, QtWidgets

from qt import about, disabled_widget, options


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


class OptionsDialog(QtWidgets.QDialog, options.Ui_Dialog):
    settings_saved = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(OptionsDialog, self).__init__(parent=parent)
        self.setupUi(self)

    def accept(self):
        """
        Saves the options to QSettings after the click of save Button
        """
        self.settings = QtCore.QSettings('BisonCorps', 'signalum')
        self.settings.setValue('bt', self.bluetoothSwitch.isChecked())
        self.settings.setValue('wf', self.wifiSwitch.isChecked())
        self.settings.setValue(
            'bt_ref_rate', self.bluetoothRefreshRate.value())
        self.settings.setValue('wifi_ref_rate', self.wifiRefreshRate.value())
        self.settings.setValue(
            'bt_services', self.showBluetoothServices.isChecked())
        self.settings.setValue('bt_names', self.showBluetoothNames.isChecked())
        success = QtWidgets.QMessageBox.information(
            self, 'Signalum Desktop', 'Changes Saved Successfully')
        self.settings_saved.emit()
        super(OptionsDialog, self).accept()


class AboutDialog(QtWidgets.QDialog, about.Ui_Dialog):
    """ Displays the about Dialog"""

    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent=parent)
        self.setupUi(self)
