# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ime/ui/ui_identifier_list.ui'
#
# Created by: PyQt6 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_IdentifierList(object):
    def setupUi(self, IdentifierList):
        IdentifierList.setObjectName("IdentifierList")
        IdentifierList.resize(748, 300)
        IdentifierList.setMaximumSize(QtCore.QSize(16777215, 350))
        self.gridLayout = QtWidgets.QGridLayout(IdentifierList)
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.btnAdd = QtWidgets.QPushButton(IdentifierList)
        self.btnAdd.setObjectName("btnAdd")
        self.gridLayout.addWidget(self.btnAdd, 1, 0, 1, 1)
        self.btnDelete = QtWidgets.QPushButton(IdentifierList)
        self.btnDelete.setObjectName("btnDelete")
        self.gridLayout.addWidget(self.btnDelete, 1, 1, 1, 1)
        self.identifierList = QtWidgets.QListView(IdentifierList)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.identifierList.sizePolicy().hasHeightForWidth())
        self.identifierList.setSizePolicy(sizePolicy)
        self.identifierList.setObjectName("identifierList")
        self.gridLayout.addWidget(self.identifierList, 0, 0, 1, 2)

        self.retranslateUi(IdentifierList)
        QtCore.QMetaObject.connectSlotsByName(IdentifierList)

    def retranslateUi(self, IdentifierList):
        _translate = QtCore.QCoreApplication.translate
        IdentifierList.setWindowTitle(_translate("IdentifierList", "Form"))
        self.btnAdd.setText(_translate("IdentifierList", "Add..."))
        self.btnDelete.setText(_translate("IdentifierList", "Remove"))
        self.identifierList.setWhatsThis(_translate("IdentifierList", "You can associate identifiers that are project-specific or externally assigned to help you distinguish the object from another, such as a RAID (Research Activity Identifier). There must be at least one identifier."))
