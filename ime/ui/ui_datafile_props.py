# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_datafile_props.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGridLayout, QLabel,
    QLineEdit, QSizePolicy, QToolBox, QWidget)

from ime.widgets.metadata_tab import MetadataTab
from ime.widgets.overridable_access_control_tab import OverridableAccessControlTab

class Ui_DatafilePropertyEditor(object):
    def setupUi(self, DatafilePropertyEditor):
        if not DatafilePropertyEditor.objectName():
            DatafilePropertyEditor.setObjectName(u"DatafilePropertyEditor")
        DatafilePropertyEditor.resize(1205, 610)
        self.gridLayout = QGridLayout(DatafilePropertyEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.toolBox_4 = QToolBox(DatafilePropertyEditor)
        self.toolBox_4.setObjectName(u"toolBox_4")
        self.toolBox_4.setMinimumSize(QSize(500, 0))
        self.fileinfoDescription = QWidget()
        self.fileinfoDescription.setObjectName(u"fileinfoDescription")
        self.fileinfoDescription.setGeometry(QRect(0, 0, 1181, 484))
        self.gridLayout_7 = QGridLayout(self.fileinfoDescription)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.formLayout_7 = QFormLayout()
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.fileInfoFilenameLabel = QLabel(self.fileinfoDescription)
        self.fileInfoFilenameLabel.setObjectName(u"fileInfoFilenameLabel")

        self.formLayout_7.setWidget(0, QFormLayout.LabelRole, self.fileInfoFilenameLabel)

        self.fileInfoFilenameLineEdit = QLineEdit(self.fileinfoDescription)
        self.fileInfoFilenameLineEdit.setObjectName(u"fileInfoFilenameLineEdit")
        self.fileInfoFilenameLineEdit.setEnabled(False)

        self.formLayout_7.setWidget(0, QFormLayout.FieldRole, self.fileInfoFilenameLineEdit)


        self.gridLayout_7.addLayout(self.formLayout_7, 0, 0, 1, 1)

        self.toolBox_4.addItem(self.fileinfoDescription, u"General")
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.page_10.setGeometry(QRect(0, 0, 1181, 484))
        self.gridLayout_2 = QGridLayout(self.page_10)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.accessControlTab = OverridableAccessControlTab(self.page_10)
        self.accessControlTab.setObjectName(u"accessControlTab")

        self.gridLayout_2.addWidget(self.accessControlTab, 0, 0, 1, 1)

        self.toolBox_4.addItem(self.page_10, u"Group access")
        self.metadata_tab = MetadataTab()
        self.metadata_tab.setObjectName(u"metadata_tab")
        self.metadata_tab.setGeometry(QRect(0, 0, 1181, 484))
        self.toolBox_4.addItem(self.metadata_tab, u"Metadata")

        self.gridLayout.addWidget(self.toolBox_4, 0, 0, 1, 1)


        self.retranslateUi(DatafilePropertyEditor)

        self.toolBox_4.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(DatafilePropertyEditor)
    # setupUi

    def retranslateUi(self, DatafilePropertyEditor):
        DatafilePropertyEditor.setWindowTitle(QCoreApplication.translate("DatafilePropertyEditor", u"Form", None))
        self.fileInfoFilenameLabel.setText(QCoreApplication.translate("DatafilePropertyEditor", u"Filename", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.fileinfoDescription), QCoreApplication.translate("DatafilePropertyEditor", u"General", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_10), QCoreApplication.translate("DatafilePropertyEditor", u"Group access", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.metadata_tab), QCoreApplication.translate("DatafilePropertyEditor", u"Metadata", None))
    # retranslateUi

