# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_DM_ManagerTeams.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DM_Manager(object):
    def setupUi(self, DM_Manager):
        DM_Manager.setObjectName("DM_Manager")
        DM_Manager.resize(822, 337)
        DM_Manager.setStyleSheet("background-color: #282828;")
        self.layoutWidget = QtWidgets.QWidget(DM_Manager)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 50, 511, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelLink = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelLink.setFont(font)
        self.labelLink.setStyleSheet("color: rgb(0, 170, 255);")
        self.labelLink.setObjectName("labelLink")
        self.horizontalLayout.addWidget(self.labelLink)
        self.lineEditLinkTournament = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditLinkTournament.sizePolicy().hasHeightForWidth())
        self.lineEditLinkTournament.setSizePolicy(sizePolicy)
        self.lineEditLinkTournament.setMaximumSize(QtCore.QSize(16777215, 27))
        self.lineEditLinkTournament.setBaseSize(QtCore.QSize(0, 0))
        self.lineEditLinkTournament.setStyleSheet("color: white;\n"
"background-color:rgb(66, 66, 66);\n"
"font: 75 10pt \"Montserrat\";")
        self.lineEditLinkTournament.setObjectName("lineEditLinkTournament")
        self.horizontalLayout.addWidget(self.lineEditLinkTournament)

        self.retranslateUi(DM_Manager)
        QtCore.QMetaObject.connectSlotsByName(DM_Manager)

    def retranslateUi(self, DM_Manager):
        _translate = QtCore.QCoreApplication.translate
        DM_Manager.setWindowTitle(_translate("DM_Manager", "Data Manager"))
        self.labelLink.setText(_translate("DM_Manager", "Link tournament:"))
