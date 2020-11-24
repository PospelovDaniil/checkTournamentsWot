# -*- coding: utf-8 -*-

from UI_DM_ManagerTeams import Ui_DM_Manager
from PyQt5 import QtCore, QtGui, QtWidgets

class DM_ManagerTeams(QtWidgets.QDialog):
    def __init__(self):
        super(DM_ManagerTeams, self).__init__()
        self.ui = Ui_DM_Manager()
        self.ui.setupUi(self)