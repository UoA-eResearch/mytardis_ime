# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ime/ui/ui_dataset_props.ui'
#
# Created by: PyQt6 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame

class Ui_DatasetProps(object):
    def setupUi(self, DatasetProps):
        DatasetProps.setObjectName("DatasetProps")
        DatasetProps.resize(560, 648)
        self.gridLayout_2 = QtWidgets.QGridLayout(DatasetProps)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.datasetTabProps = QtWidgets.QStackedWidget(DatasetProps)
        self.datasetTabProps.setObjectName("datasetTabProps")
        self.datasetProperties = QtWidgets.QWidget()
        self.datasetProperties.setObjectName("datasetProperties")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.datasetProperties)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.toolBox = QtWidgets.QToolBox(self.datasetProperties)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QtCore.QSize(500, 0))
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 548, 528))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy)
        self.page.setObjectName("page")
        self.formLayout = QtWidgets.QFormLayout(self.page)
        self.formLayout.setObjectName("formLayout")
        self.label_21 = QtWidgets.QLabel(self.page)
        self.label_21.setObjectName("label_21")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_21)
        self.datasetNameLineEdit = QtWidgets.QLineEdit(self.page)
        self.datasetNameLineEdit.setText("")
        self.datasetNameLineEdit.setObjectName("datasetNameLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.datasetNameLineEdit)
        self.label_24 = QtWidgets.QLabel(self.page)
        self.label_24.setObjectName("label_24")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_24)
        self.instrumentIDLineEdit = QtWidgets.QLineEdit(self.page)
        self.instrumentIDLineEdit.setObjectName("instrumentIDLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.instrumentIDLineEdit)
        self.label = QtWidgets.QLabel(self.page)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.identifierList = IdentifierList(self.page)
        self.identifierList.setObjectName("identifierList")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.identifierList)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.ItemRole.FieldRole, spacerItem)
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 548, 516))
        self.page_2.setObjectName("page_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.accessControlTab = OverridableAccessControlTab(self.page_2)
        self.accessControlTab.setObjectName("accessControlTab")
        self.verticalLayout.addWidget(self.accessControlTab)
        self.toolBox.addItem(self.page_2, "")
        self.page_3 = MetadataTab()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 548, 516))
        self.page_3.setObjectName("page_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.toolBox.addItem(self.page_3, "")
        self.gridLayout_6.addWidget(self.toolBox, 0, 0, 1, 1)
        self.datasetTabProps.addWidget(self.datasetProperties)
        self.datafileProperties = QtWidgets.QWidget()
        self.datafileProperties.setObjectName("datafileProperties")
        self.gridLayout = QtWidgets.QGridLayout(self.datafileProperties)
        self.gridLayout.setObjectName("gridLayout")
        self.toolBox_4 = QtWidgets.QToolBox(self.datafileProperties)
        self.toolBox_4.setMinimumSize(QtCore.QSize(500, 0))
        self.toolBox_4.setObjectName("toolBox_4")
        self.fileinfoDescription = QtWidgets.QWidget()
        self.fileinfoDescription.setGeometry(QtCore.QRect(0, 0, 486, 50))
        self.fileinfoDescription.setObjectName("fileinfoDescription")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.fileinfoDescription)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setObjectName("formLayout_7")
        self.fileInfoFilenameLabel = QtWidgets.QLabel(self.fileinfoDescription)
        self.fileInfoFilenameLabel.setObjectName("fileInfoFilenameLabel")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.fileInfoFilenameLabel)
        self.fileInfoFilenameLineEdit = QtWidgets.QLineEdit(self.fileinfoDescription)
        self.fileInfoFilenameLineEdit.setObjectName("fileInfoFilenameLineEdit")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.fileInfoFilenameLineEdit)
        self.gridLayout_7.addLayout(self.formLayout_7, 0, 0, 1, 1)
        self.toolBox_4.addItem(self.fileinfoDescription, "")
        self.page_10 = QtWidgets.QWidget()
        self.page_10.setGeometry(QtCore.QRect(0, 0, 334, 640))
        self.page_10.setObjectName("page_10")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.checkBox_3 = QtWidgets.QCheckBox(self.page_10)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_5.addWidget(self.checkBox_3)
        self.frame_5 = QtWidgets.QFrame(self.page_10)
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.formLayout_6 = QtWidgets.QFormLayout(self.frame_5)
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_36 = QtWidgets.QLabel(self.frame_5)
        self.label_36.setObjectName("label_36")
        self.formLayout_6.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_36)
        self.tableWidget_23 = QtWidgets.QTableWidget(self.frame_5)
        self.tableWidget_23.setEnabled(False)
        self.tableWidget_23.setObjectName("tableWidget_23")
        self.tableWidget_23.setColumnCount(0)
        self.tableWidget_23.setRowCount(0)
        self.formLayout_6.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tableWidget_23)
        self.label_37 = QtWidgets.QLabel(self.frame_5)
        self.label_37.setObjectName("label_37")
        self.formLayout_6.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_37)
        self.tableWidget_24 = QtWidgets.QTableWidget(self.frame_5)
        self.tableWidget_24.setEnabled(False)
        self.tableWidget_24.setObjectName("tableWidget_24")
        self.tableWidget_24.setColumnCount(0)
        self.tableWidget_24.setRowCount(0)
        self.formLayout_6.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tableWidget_24)
        self.label_38 = QtWidgets.QLabel(self.frame_5)
        self.label_38.setObjectName("label_38")
        self.formLayout_6.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_38)
        self.tableWidget_25 = QtWidgets.QTableWidget(self.frame_5)
        self.tableWidget_25.setEnabled(False)
        self.tableWidget_25.setObjectName("tableWidget_25")
        self.tableWidget_25.setColumnCount(0)
        self.tableWidget_25.setRowCount(0)
        self.formLayout_6.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tableWidget_25)
        self.label_39 = QtWidgets.QLabel(self.frame_5)
        self.label_39.setObjectName("label_39")
        self.formLayout_6.setWidget(8, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_39)
        self.tableWidget_26 = QtWidgets.QTableWidget(self.frame_5)
        self.tableWidget_26.setEnabled(False)
        self.tableWidget_26.setObjectName("tableWidget_26")
        self.tableWidget_26.setColumnCount(0)
        self.tableWidget_26.setRowCount(0)
        self.formLayout_6.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tableWidget_26)
        self.label_40 = QtWidgets.QLabel(self.frame_5)
        self.label_40.setObjectName("label_40")
        self.formLayout_6.setWidget(10, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_40)
        self.tableWidget_27 = QtWidgets.QTableWidget(self.frame_5)
        self.tableWidget_27.setEnabled(False)
        self.tableWidget_27.setObjectName("tableWidget_27")
        self.tableWidget_27.setColumnCount(0)
        self.tableWidget_27.setRowCount(0)
        self.formLayout_6.setWidget(10, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tableWidget_27)
        self.label_41 = QtWidgets.QLabel(self.frame_5)
        self.label_41.setObjectName("label_41")
        self.formLayout_6.setWidget(12, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_41)
        self.tableWidget_28 = QtWidgets.QTableWidget(self.frame_5)
        self.tableWidget_28.setEnabled(False)
        self.tableWidget_28.setObjectName("tableWidget_28")
        self.tableWidget_28.setColumnCount(0)
        self.tableWidget_28.setRowCount(0)
        self.formLayout_6.setWidget(12, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tableWidget_28)
        self.label_42 = QtWidgets.QLabel(self.frame_5)
        self.label_42.setObjectName("label_42")
        self.formLayout_6.setWidget(14, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_42)
        self.tableWidget_29 = QtWidgets.QTableWidget(self.frame_5)
        self.tableWidget_29.setEnabled(False)
        self.tableWidget_29.setObjectName("tableWidget_29")
        self.tableWidget_29.setColumnCount(0)
        self.tableWidget_29.setRowCount(0)
        self.formLayout_6.setWidget(14, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tableWidget_29)
        self.verticalLayout_5.addWidget(self.frame_5)
        self.toolBox_4.addItem(self.page_10, "")
        self.page_11 = QtWidgets.QWidget()
        self.page_11.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.page_11.setObjectName("page_11")
        self.toolBox_4.addItem(self.page_11, "")
        self.gridLayout.addWidget(self.toolBox_4, 0, 0, 1, 1)
        self.datasetTabProps.addWidget(self.datafileProperties)
        self.noDatasetSelectedProps = QtWidgets.QWidget()
        self.noDatasetSelectedProps.setObjectName("noDatasetSelectedProps")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.noDatasetSelectedProps)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.label_43 = QtWidgets.QLabel(self.noDatasetSelectedProps)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy)
        self.label_43.setMinimumSize(QtCore.QSize(0, 0))
        self.label_43.setMaximumSize(QtCore.QSize(200, 200))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_43.setFont(font)
        self.label_43.setText("")
        self.label_43.setPixmap(QtGui.QPixmap(":/resources/noun-empty-2900960.svg"))
        self.label_43.setScaledContents(True)
        self.label_43.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label_43.setObjectName("label_43")
        self.verticalLayout_3.addWidget(self.label_43, 0, Qt.AlignmentFlag.AlignHCenter)
        self.label_44 = QtWidgets.QLabel(self.noDatasetSelectedProps)
        font = QtGui.QFont()
        font.setFamily("Noto Sans Display")
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label_44.setFont(font)
        self.label_44.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_44.setObjectName("label_44")
        self.verticalLayout_3.addWidget(self.label_44)
        self.label_45 = QtWidgets.QLabel(self.noDatasetSelectedProps)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(12)
        self.label_45.setFont(font)
        self.label_45.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_45.setWordWrap(True)
        self.label_45.setObjectName("label_45")
        self.verticalLayout_3.addWidget(self.label_45)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.gridLayout_8.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.datasetTabProps.addWidget(self.noDatasetSelectedProps)
        self.gridLayout_2.addWidget(self.datasetTabProps, 0, 0, 1, 1)

        self.retranslateUi(DatasetProps)
        self.datasetTabProps.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        self.toolBox_4.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DatasetProps)

    def retranslateUi(self, DatasetProps):
        _translate = QtCore.QCoreApplication.translate
        DatasetProps.setWindowTitle(_translate("DatasetProps", "Form"))
        self.label_21.setText(_translate("DatasetProps", "Dataset name"))
        self.datasetNameLineEdit.setPlaceholderText(_translate("DatasetProps", "The dataset name"))
        self.label_24.setText(_translate("DatasetProps", "Instrument ID"))
        self.instrumentIDLineEdit.setPlaceholderText(_translate("DatasetProps", "A unique identifier to the instrument that the data was generated on. Currently there is no standard persistent identifier that has widespread community adoption (DOIs are the most likely candidate)."))
        self.label.setText(_translate("DatasetProps", "Identifiers"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("DatasetProps", "General"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("DatasetProps", "User and group access"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("DatasetProps", "Metadata"))
        self.fileInfoFilenameLabel.setText(_translate("DatasetProps", "Filename"))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.fileinfoDescription), _translate("DatasetProps", "Description"))
        self.checkBox_3.setText(_translate("DatasetProps", "Override Dataset user and group settings"))
        self.label_36.setText(_translate("DatasetProps", "Admin groups"))
        self.label_37.setText(_translate("DatasetProps", "Admin users"))
        self.label_38.setText(_translate("DatasetProps", "Read groups"))
        self.label_39.setText(_translate("DatasetProps", "Read users"))
        self.label_40.setText(_translate("DatasetProps", "Download groups"))
        self.label_41.setText(_translate("DatasetProps", "Download users"))
        self.label_42.setText(_translate("DatasetProps", "Sensitive groups"))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_10), _translate("DatasetProps", "Users and groups"))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_11), _translate("DatasetProps", "Metadata"))
        self.label_44.setText(_translate("DatasetProps", "No dataset or file selected."))
        self.label_45.setText(_translate("DatasetProps", "Select a dataset or file to edit metadata and access controls."))
from ime.widgets.identifier_list import IdentifierList
from ime.widgets.metadata_tab import MetadataTab
from ime.widgets.overridable_access_control_tab import OverridableAccessControlTab
import default_rc
