# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './disabled_widget.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(577, 183)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MessageLabel = QtWidgets.QLabel(Form)
        self.MessageLabel.setStyleSheet("font: 75 16pt \"Ubuntu\";")
        self.MessageLabel.setObjectName("MessageLabel")
        self.verticalLayout.addWidget(self.MessageLabel)
        self.MessageBodyLabel = QtWidgets.QLabel(Form)
        self.MessageBodyLabel.setStyleSheet("font: 75 14pt \"Ubuntu\";")
        self.MessageBodyLabel.setObjectName("MessageBodyLabel")
        self.verticalLayout.addWidget(self.MessageBodyLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.MessageLabel.setText(_translate("Form", "Bluetooth Mode is Disabled"))
        self.MessageBodyLabel.setText(_translate("Form", "Enable it in your settings and ensure your driver is enabled as well"))


