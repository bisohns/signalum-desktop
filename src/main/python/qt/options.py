# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './options.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(583, 359)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.showBluetoothServices = QtWidgets.QCheckBox(Dialog)
        self.showBluetoothServices.setObjectName("showBluetoothServices")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.showBluetoothServices)
        self.showBluetoothNames = QtWidgets.QCheckBox(Dialog)
        self.showBluetoothNames.setChecked(True)
        self.showBluetoothNames.setObjectName("showBluetoothNames")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.showBluetoothNames)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.bluetoothRefreshRate = QtWidgets.QSpinBox(Dialog)
        self.bluetoothRefreshRate.setMinimum(1)
        self.bluetoothRefreshRate.setMaximum(60)
        self.bluetoothRefreshRate.setSingleStep(1)
        self.bluetoothRefreshRate.setProperty("value", 1)
        self.bluetoothRefreshRate.setObjectName("bluetoothRefreshRate")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.bluetoothRefreshRate)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.wifiRefreshRate = QtWidgets.QSpinBox(Dialog)
        self.wifiRefreshRate.setMinimum(1)
        self.wifiRefreshRate.setMaximum(60)
        self.wifiRefreshRate.setSingleStep(1)
        self.wifiRefreshRate.setProperty("value", 1)
        self.wifiRefreshRate.setObjectName("wifiRefreshRate")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.wifiRefreshRate)
        self.wifiSwitch = QtWidgets.QCheckBox(Dialog)
        self.wifiSwitch.setEnabled(True)
        self.wifiSwitch.setChecked(False)
        self.wifiSwitch.setObjectName("wifiSwitch")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.wifiSwitch)
        self.bluetoothSwitch = QtWidgets.QCheckBox(Dialog)
        self.bluetoothSwitch.setChecked(False)
        self.bluetoothSwitch.setObjectName("bluetoothSwitch")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.bluetoothSwitch)
        self.darkModeCheckBox = QtWidgets.QCheckBox(Dialog)
        self.darkModeCheckBox.setChecked(True)
        self.darkModeCheckBox.setObjectName("darkModeCheckBox")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.darkModeCheckBox)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.showBluetoothServices.setText(_translate("Dialog", "Show bluetooth services"))
        self.showBluetoothNames.setText(_translate("Dialog", "Show bluetooth names"))
        self.label_2.setText(_translate("Dialog", "Bluetooth Device Refresh rate (sec)"))
        self.label_7.setText(_translate("Dialog", "WiFi Device Refresh rate (sec)"))
        self.wifiSwitch.setText(_translate("Dialog", "Turn Wifi on"))
        self.bluetoothSwitch.setText(_translate("Dialog", "Turn Bluetooth on"))
        self.darkModeCheckBox.setText(_translate("Dialog", "Dark Mode"))


