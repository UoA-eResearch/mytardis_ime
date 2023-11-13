# Form implementation generated from reading ui file 'ime/ui/ui_experiment_props.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ExperimentPropertyEditor(object):
    def setupUi(self, ExperimentPropertyEditor):
        ExperimentPropertyEditor.setObjectName("ExperimentPropertyEditor")
        ExperimentPropertyEditor.resize(518, 487)
        self.gridLayout = QtWidgets.QGridLayout(ExperimentPropertyEditor)
        self.gridLayout.setObjectName("gridLayout")
        self.toolBox_2 = QtWidgets.QToolBox(parent=ExperimentPropertyEditor)
        self.toolBox_2.setMinimumSize(QtCore.QSize(500, 0))
        self.toolBox_2.setObjectName("toolBox_2")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 506, 367))
        self.page_4.setObjectName("page_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_18 = QtWidgets.QLabel(parent=self.page_4)
        self.label_18.setObjectName("label_18")
        self.gridLayout_3.addWidget(self.label_18, 1, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(parent=self.page_4)
        self.label_19.setObjectName("label_19")
        self.gridLayout_3.addWidget(self.label_19, 2, 0, 1, 1)
        self.experimentNameLineEdit = QtWidgets.QLineEdit(parent=self.page_4)
        self.experimentNameLineEdit.setObjectName("experimentNameLineEdit")
        self.gridLayout_3.addWidget(self.experimentNameLineEdit, 0, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(parent=self.page_4)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 0, 0, 1, 1)
        self.identifierList = IdentifierList(parent=self.page_4)
        self.identifierList.setObjectName("identifierList")
        self.gridLayout_3.addWidget(self.identifierList, 1, 1, 1, 1)
        self.experimentDescriptionLineEdit = QtWidgets.QPlainTextEdit(parent=self.page_4)
        self.experimentDescriptionLineEdit.setObjectName("experimentDescriptionLineEdit")
        self.gridLayout_3.addWidget(self.experimentDescriptionLineEdit, 2, 1, 1, 1)
        self.toolBox_2.addItem(self.page_4, "")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0, 0, 506, 367))
        self.page_5.setObjectName("page_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.accessControlTab = OverridableAccessControlTab(parent=self.page_5)
        self.accessControlTab.setObjectName("accessControlTab")
        self.verticalLayout_4.addWidget(self.accessControlTab)
        self.toolBox_2.addItem(self.page_5, "")
        self.metadata_tab = MetadataTab()
        self.metadata_tab.setGeometry(QtCore.QRect(0, 0, 506, 367))
        self.metadata_tab.setObjectName("metadata_tab")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.metadata_tab)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.toolBox_2.addItem(self.metadata_tab, "")
        self.gridLayout.addWidget(self.toolBox_2, 0, 0, 1, 1)

        self.retranslateUi(ExperimentPropertyEditor)
        self.toolBox_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ExperimentPropertyEditor)

    def retranslateUi(self, ExperimentPropertyEditor):
        _translate = QtCore.QCoreApplication.translate
        ExperimentPropertyEditor.setWindowTitle(_translate("ExperimentPropertyEditor", "Form"))
        self.label_18.setText(_translate("ExperimentPropertyEditor", "Identifiers"))
        self.label_19.setText(_translate("ExperimentPropertyEditor", "Description"))
        self.label_15.setText(_translate("ExperimentPropertyEditor", "Experiment name"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_4), _translate("ExperimentPropertyEditor", "General"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_5), _translate("ExperimentPropertyEditor", "User and group access"))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.metadata_tab), _translate("ExperimentPropertyEditor", "Metadata"))
from ime.widgets.identifier_list import IdentifierList
from ime.widgets.metadata_tab import MetadataTab
from ime.widgets.overridable_access_control_tab import OverridableAccessControlTab
