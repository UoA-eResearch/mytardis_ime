# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ime/ui/ui_access_control_list.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AccessControlList(object):
    def setupUi(self, AccessControlList):
        AccessControlList.setObjectName("AccessControlList")
        AccessControlList.resize(471, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(AccessControlList.sizePolicy().hasHeightForWidth())
        AccessControlList.setSizePolicy(sizePolicy)
        AccessControlList.setMinimumSize(QtCore.QSize(0, 150))
        self.gridLayout = QtWidgets.QGridLayout(AccessControlList)
        self.gridLayout.setContentsMargins(-1, -1, -1, 9)
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.aclList = QtWidgets.QListView(AccessControlList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aclList.sizePolicy().hasHeightForWidth())
        self.aclList.setSizePolicy(sizePolicy)
        self.aclList.setObjectName("aclList")
        self.horizontalLayout_2.addWidget(self.aclList)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnAdd = QtWidgets.QPushButton(AccessControlList)
        self.btnAdd.setObjectName("btnAdd")
        self.verticalLayout_2.addWidget(self.btnAdd)
        self.btnDelete = QtWidgets.QPushButton(AccessControlList)
        self.btnDelete.setObjectName("btnDelete")
        self.verticalLayout_2.addWidget(self.btnDelete)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.overrideCheckBox = QtWidgets.QCheckBox(AccessControlList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.overrideCheckBox.sizePolicy().hasHeightForWidth())
        self.overrideCheckBox.setSizePolicy(sizePolicy)
        self.overrideCheckBox.setObjectName("overrideCheckBox")
        self.gridLayout.addWidget(self.overrideCheckBox, 0, 0, 1, 1)

        self.retranslateUi(AccessControlList)
        QtCore.QMetaObject.connectSlotsByName(AccessControlList)

    def retranslateUi(self, AccessControlList):
        _translate = QtCore.QCoreApplication.translate
        AccessControlList.setWindowTitle(_translate("AccessControlList", "Form"))
        self.btnAdd.setText(_translate("AccessControlList", "Add"))
        self.btnDelete.setText(_translate("AccessControlList", "Delete"))
        self.overrideCheckBox.setText(_translate("AccessControlList", "Override inherited properties"))
