# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ime/ui/ui_project_access_control_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ProjectAccessControlTab(object):
    def setupUi(self, ProjectAccessControlTab):
        ProjectAccessControlTab.setObjectName("ProjectAccessControlTab")
        ProjectAccessControlTab.resize(725, 1080)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(ProjectAccessControlTab.sizePolicy().hasHeightForWidth())
        ProjectAccessControlTab.setSizePolicy(sizePolicy)
        ProjectAccessControlTab.setMinimumSize(QtCore.QSize(400, 500))
        self.verticalLayout = QtWidgets.QVBoxLayout(ProjectAccessControlTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(ProjectAccessControlTab)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ProjectAccessControlTab)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.groups = AccessControlList(ProjectAccessControlTab)
        self.groups.setObjectName("groups")
        self.gridLayout.addWidget(self.groups, 2, 1, 1, 1)
        self.users = AccessControlList(ProjectAccessControlTab)
        self.users.setObjectName("users")
        self.gridLayout.addWidget(self.users, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ProjectAccessControlTab)
        QtCore.QMetaObject.connectSlotsByName(ProjectAccessControlTab)

    def retranslateUi(self, ProjectAccessControlTab):
        _translate = QtCore.QCoreApplication.translate
        ProjectAccessControlTab.setWindowTitle(_translate("ProjectAccessControlTab", "Form"))
        self.label.setText(_translate("ProjectAccessControlTab", "Users"))
        self.label_2.setText(_translate("ProjectAccessControlTab", "Groups"))
from ime.widgets.access_control_list import AccessControlList
