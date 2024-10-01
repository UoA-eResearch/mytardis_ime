# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_project_props.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QLabel, QLineEdit, QPlainTextEdit, QSizePolicy,
    QToolBox, QWidget)

from ime.widgets.identifier_list import IdentifierList
from ime.widgets.metadata_tab import MetadataTab
from ime.widgets.project_access_control_tab import ProjectAccessControlTab

class Ui_ProjectPropertyEditor(object):
    def setupUi(self, ProjectPropertyEditor):
        if not ProjectPropertyEditor.objectName():
            ProjectPropertyEditor.setObjectName(u"ProjectPropertyEditor")
        ProjectPropertyEditor.resize(524, 553)
        self.gridLayout = QGridLayout(ProjectPropertyEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.toolBox_3 = QToolBox(ProjectPropertyEditor)
        self.toolBox_3.setObjectName(u"toolBox_3")
        self.toolBox_3.setMinimumSize(QSize(500, 0))
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.page_7.setGeometry(QRect(0, 0, 500, 427))
        self.gridLayout_2 = QGridLayout(self.page_7)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame_3 = QFrame(self.page_7)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.formLayout_4 = QFormLayout(self.frame_3)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.projectNameLineEdit = QLineEdit(self.frame_3)
        self.projectNameLineEdit.setObjectName(u"projectNameLineEdit")

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.projectNameLineEdit)

        self.label_5 = QLabel(self.frame_3)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.label_27 = QLabel(self.frame_3)
        self.label_27.setObjectName(u"label_27")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_27)

        self.projectDescriptionLineEdit = QPlainTextEdit(self.frame_3)
        self.projectDescriptionLineEdit.setObjectName(u"projectDescriptionLineEdit")

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.projectDescriptionLineEdit)

        self.leadResearcherLabel = QLabel(self.frame_3)
        self.leadResearcherLabel.setObjectName(u"leadResearcherLabel")

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.leadResearcherLabel)

        self.leadResearcherLineEdit = QLineEdit(self.frame_3)
        self.leadResearcherLineEdit.setObjectName(u"leadResearcherLineEdit")

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.leadResearcherLineEdit)

        self.identifierList = IdentifierList(self.frame_3)
        self.identifierList.setObjectName(u"identifierList")

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.identifierList)


        self.gridLayout_2.addWidget(self.frame_3, 0, 0, 1, 1)

        self.toolBox_3.addItem(self.page_7, u"General")
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.page_8.setGeometry(QRect(0, 0, 500, 427))
        self.gridLayout_4 = QGridLayout(self.page_8)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.accessControlTab = ProjectAccessControlTab(self.page_8)
        self.accessControlTab.setObjectName(u"accessControlTab")

        self.gridLayout_4.addWidget(self.accessControlTab, 0, 0, 1, 1)

        self.toolBox_3.addItem(self.page_8, u"Group access")
        self.metadata_tab = MetadataTab()
        self.metadata_tab.setObjectName(u"metadata_tab")
        self.metadata_tab.setGeometry(QRect(0, 0, 98, 28))
        self.gridLayout_5 = QGridLayout(self.metadata_tab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.toolBox_3.addItem(self.metadata_tab, u"Metadata")

        self.gridLayout.addWidget(self.toolBox_3, 0, 0, 1, 1)


        self.retranslateUi(ProjectPropertyEditor)

        self.toolBox_3.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(ProjectPropertyEditor)
    # setupUi

    def retranslateUi(self, ProjectPropertyEditor):
        ProjectPropertyEditor.setWindowTitle(QCoreApplication.translate("ProjectPropertyEditor", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("ProjectPropertyEditor", u"Project name", None))
        self.label_5.setText(QCoreApplication.translate("ProjectPropertyEditor", u"Identifiers", None))
        self.label_27.setText(QCoreApplication.translate("ProjectPropertyEditor", u"Description", None))
        self.leadResearcherLabel.setText(QCoreApplication.translate("ProjectPropertyEditor", u"Principal Investigator", None))
        self.toolBox_3.setItemText(self.toolBox_3.indexOf(self.page_7), QCoreApplication.translate("ProjectPropertyEditor", u"General", None))
        self.toolBox_3.setItemText(self.toolBox_3.indexOf(self.page_8), QCoreApplication.translate("ProjectPropertyEditor", u"Group access", None))
        self.toolBox_3.setItemText(self.toolBox_3.indexOf(self.metadata_tab), QCoreApplication.translate("ProjectPropertyEditor", u"Metadata", None))
    # retranslateUi

