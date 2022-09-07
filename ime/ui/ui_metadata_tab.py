# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ime/ui/ui_metadata_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MetadataTab(object):
    def setupUi(self, MetadataTab):
        MetadataTab.setObjectName("MetadataTab")
        MetadataTab.resize(766, 639)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MetadataTab.sizePolicy().hasHeightForWidth())
        MetadataTab.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(MetadataTab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(MetadataTab)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(MetadataTab)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.widget = QtWidgets.QWidget(MetadataTab)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.remove_rows_btn = QtWidgets.QPushButton(self.widget)
        self.remove_rows_btn.setEnabled(False)
        self.remove_rows_btn.setObjectName("remove_rows_btn")
        self.horizontalLayout_2.addWidget(self.remove_rows_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.widget)
        self.metadata_table = QtWidgets.QTableWidget(MetadataTab)
        self.metadata_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.metadata_table.setObjectName("metadata_table")
        self.metadata_table.setColumnCount(2)
        self.metadata_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.metadata_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.metadata_table.setHorizontalHeaderItem(1, item)
        self.metadata_table.horizontalHeader().setStretchLastSection(True)
        self.metadata_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.metadata_table)

        self.retranslateUi(MetadataTab)
        QtCore.QMetaObject.connectSlotsByName(MetadataTab)

    def retranslateUi(self, MetadataTab):
        _translate = QtCore.QCoreApplication.translate
        MetadataTab.setWindowTitle(_translate("MetadataTab", "Form"))
        self.label.setText(_translate("MetadataTab", "You can add metadata to help you and your collaborators remember the conditions in which the data was produced. You can also create schemas in MyTardis that specify standard fields to fill in."))
        self.label_2.setText(_translate("MetadataTab", "Schema: None"))
        self.remove_rows_btn.setText(_translate("MetadataTab", "Remove"))
        item = self.metadata_table.horizontalHeaderItem(0)
        item.setText(_translate("MetadataTab", "Metadata name"))
        item = self.metadata_table.horizontalHeaderItem(1)
        item.setText(_translate("MetadataTab", "Value"))
