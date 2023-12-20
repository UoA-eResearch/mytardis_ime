# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_experiment_props.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPlainTextEdit, QSizePolicy, QToolBox, QVBoxLayout,
    QWidget)

from ime.widgets.identifier_list import IdentifierList
from ime.widgets.metadata_tab import MetadataTab
from ime.widgets.overridable_access_control_tab import OverridableAccessControlTab

class Ui_ExperimentPropertyEditor(object):
    def setupUi(self, ExperimentPropertyEditor):
        if not ExperimentPropertyEditor.objectName():
            ExperimentPropertyEditor.setObjectName(u"ExperimentPropertyEditor")
        ExperimentPropertyEditor.resize(518, 487)
        self.gridLayout = QGridLayout(ExperimentPropertyEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.toolBox_2 = QToolBox(ExperimentPropertyEditor)
        self.toolBox_2.setObjectName(u"toolBox_2")
        self.toolBox_2.setMinimumSize(QSize(500, 0))
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4.setGeometry(QRect(0, 0, 506, 367))
        self.gridLayout_3 = QGridLayout(self.page_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_18 = QLabel(self.page_4)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_3.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_19 = QLabel(self.page_4)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_3.addWidget(self.label_19, 2, 0, 1, 1)

        self.experimentNameLineEdit = QLineEdit(self.page_4)
        self.experimentNameLineEdit.setObjectName(u"experimentNameLineEdit")

        self.gridLayout_3.addWidget(self.experimentNameLineEdit, 0, 1, 1, 1)

        self.label_15 = QLabel(self.page_4)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_3.addWidget(self.label_15, 0, 0, 1, 1)

        self.identifierList = IdentifierList(self.page_4)
        self.identifierList.setObjectName(u"identifierList")

        self.gridLayout_3.addWidget(self.identifierList, 1, 1, 1, 1)

        self.experimentDescriptionLineEdit = QPlainTextEdit(self.page_4)
        self.experimentDescriptionLineEdit.setObjectName(u"experimentDescriptionLineEdit")

        self.gridLayout_3.addWidget(self.experimentDescriptionLineEdit, 2, 1, 1, 1)

        self.toolBox_2.addItem(self.page_4, u"General")
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.page_5.setGeometry(QRect(0, 0, 506, 367))
        self.verticalLayout_4 = QVBoxLayout(self.page_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.accessControlTab = OverridableAccessControlTab(self.page_5)
        self.accessControlTab.setObjectName(u"accessControlTab")

        self.verticalLayout_4.addWidget(self.accessControlTab)

        self.toolBox_2.addItem(self.page_5, u"User and group access")
        self.metadata_tab = MetadataTab()
        self.metadata_tab.setObjectName(u"metadata_tab")
        self.metadata_tab.setGeometry(QRect(0, 0, 506, 367))
        self.gridLayout_13 = QGridLayout(self.metadata_tab)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.toolBox_2.addItem(self.metadata_tab, u"Metadata")

        self.gridLayout.addWidget(self.toolBox_2, 0, 0, 1, 1)


        self.retranslateUi(ExperimentPropertyEditor)

        self.toolBox_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ExperimentPropertyEditor)
    # setupUi

    def retranslateUi(self, ExperimentPropertyEditor):
        ExperimentPropertyEditor.setWindowTitle(QCoreApplication.translate("ExperimentPropertyEditor", u"Form", None))
        self.label_18.setText(QCoreApplication.translate("ExperimentPropertyEditor", u"Identifiers", None))
        self.label_19.setText(QCoreApplication.translate("ExperimentPropertyEditor", u"Description", None))
        self.label_15.setText(QCoreApplication.translate("ExperimentPropertyEditor", u"Experiment name", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_4), QCoreApplication.translate("ExperimentPropertyEditor", u"General", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_5), QCoreApplication.translate("ExperimentPropertyEditor", u"User and group access", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.metadata_tab), QCoreApplication.translate("ExperimentPropertyEditor", u"Metadata", None))
    # retranslateUi

