# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_dataset_props.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QFrame,
    QGridLayout, QHeaderView, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QStackedWidget, QTableWidget,
    QTableWidgetItem, QToolBox, QVBoxLayout, QWidget)

from ime.widgets.identifier_list import IdentifierList
from ime.widgets.metadata_tab import MetadataTab
from ime.widgets.overridable_access_control_tab import OverridableAccessControlTab
import default_rc
import default_rc
import default_rc
import default_rc
import default_rc

class Ui_DatasetProps(object):
    def setupUi(self, DatasetProps):
        if not DatasetProps.objectName():
            DatasetProps.setObjectName(u"DatasetProps")
        DatasetProps.resize(560, 648)
        self.gridLayout_2 = QGridLayout(DatasetProps)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.datasetTabProps = QStackedWidget(DatasetProps)
        self.datasetTabProps.setObjectName(u"datasetTabProps")
        self.datasetProperties = QWidget()
        self.datasetProperties.setObjectName(u"datasetProperties")
        self.gridLayout_6 = QGridLayout(self.datasetProperties)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.toolBox = QToolBox(self.datasetProperties)
        self.toolBox.setObjectName(u"toolBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QSize(500, 0))
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 536, 522))
        sizePolicy.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(self.page)
        self.formLayout.setObjectName(u"formLayout")
        self.label_21 = QLabel(self.page)
        self.label_21.setObjectName(u"label_21")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_21)

        self.datasetNameLineEdit = QLineEdit(self.page)
        self.datasetNameLineEdit.setObjectName(u"datasetNameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.datasetNameLineEdit)

        self.label_24 = QLabel(self.page)
        self.label_24.setObjectName(u"label_24")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_24)

        self.instrumentIDLineEdit = QLineEdit(self.page)
        self.instrumentIDLineEdit.setObjectName(u"instrumentIDLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.instrumentIDLineEdit)

        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.identifierList = IdentifierList(self.page)
        self.identifierList.setObjectName(u"identifierList")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.identifierList)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(3, QFormLayout.FieldRole, self.verticalSpacer_3)

        self.toolBox.addItem(self.page, u"General")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 536, 522))
        self.verticalLayout = QVBoxLayout(self.page_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.accessControlTab = OverridableAccessControlTab(self.page_2)
        self.accessControlTab.setObjectName(u"accessControlTab")

        self.verticalLayout.addWidget(self.accessControlTab)

        self.toolBox.addItem(self.page_2, u"Group access")
        self.page_3 = MetadataTab()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setGeometry(QRect(0, 0, 536, 522))
        self.gridLayout_4 = QGridLayout(self.page_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.toolBox.addItem(self.page_3, u"Metadata")

        self.gridLayout_6.addWidget(self.toolBox, 0, 0, 1, 1)

        self.datasetTabProps.addWidget(self.datasetProperties)
        self.datafileProperties = QWidget()
        self.datafileProperties.setObjectName(u"datafileProperties")
        self.gridLayout = QGridLayout(self.datafileProperties)
        self.gridLayout.setObjectName(u"gridLayout")
        self.toolBox_4 = QToolBox(self.datafileProperties)
        self.toolBox_4.setObjectName(u"toolBox_4")
        self.toolBox_4.setMinimumSize(QSize(500, 0))
        self.fileinfoDescription = QWidget()
        self.fileinfoDescription.setObjectName(u"fileinfoDescription")
        self.fileinfoDescription.setGeometry(QRect(0, 0, 104, 47))
        self.gridLayout_7 = QGridLayout(self.fileinfoDescription)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.formLayout_7 = QFormLayout()
        self.formLayout_7.setObjectName(u"formLayout_7")
        self.fileInfoFilenameLabel = QLabel(self.fileinfoDescription)
        self.fileInfoFilenameLabel.setObjectName(u"fileInfoFilenameLabel")

        self.formLayout_7.setWidget(0, QFormLayout.LabelRole, self.fileInfoFilenameLabel)

        self.fileInfoFilenameLineEdit = QLineEdit(self.fileinfoDescription)
        self.fileInfoFilenameLineEdit.setObjectName(u"fileInfoFilenameLineEdit")

        self.formLayout_7.setWidget(0, QFormLayout.FieldRole, self.fileInfoFilenameLineEdit)


        self.gridLayout_7.addLayout(self.formLayout_7, 0, 0, 1, 1)

        self.toolBox_4.addItem(self.fileinfoDescription, u"Description")
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.page_10.setGeometry(QRect(0, 0, 289, 765))
        self.verticalLayout_5 = QVBoxLayout(self.page_10)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.checkBox_3 = QCheckBox(self.page_10)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout_5.addWidget(self.checkBox_3)

        self.frame_5 = QFrame(self.page_10)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.formLayout_6 = QFormLayout(self.frame_5)
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.label_36 = QLabel(self.frame_5)
        self.label_36.setObjectName(u"label_36")

        self.formLayout_6.setWidget(3, QFormLayout.LabelRole, self.label_36)

        self.tableWidget_23 = QTableWidget(self.frame_5)
        self.tableWidget_23.setObjectName(u"tableWidget_23")
        self.tableWidget_23.setEnabled(False)

        self.formLayout_6.setWidget(3, QFormLayout.FieldRole, self.tableWidget_23)

        self.label_37 = QLabel(self.frame_5)
        self.label_37.setObjectName(u"label_37")

        self.formLayout_6.setWidget(4, QFormLayout.LabelRole, self.label_37)

        self.tableWidget_24 = QTableWidget(self.frame_5)
        self.tableWidget_24.setObjectName(u"tableWidget_24")
        self.tableWidget_24.setEnabled(False)

        self.formLayout_6.setWidget(4, QFormLayout.FieldRole, self.tableWidget_24)

        self.label_38 = QLabel(self.frame_5)
        self.label_38.setObjectName(u"label_38")

        self.formLayout_6.setWidget(6, QFormLayout.LabelRole, self.label_38)

        self.tableWidget_25 = QTableWidget(self.frame_5)
        self.tableWidget_25.setObjectName(u"tableWidget_25")
        self.tableWidget_25.setEnabled(False)

        self.formLayout_6.setWidget(6, QFormLayout.FieldRole, self.tableWidget_25)

        self.label_39 = QLabel(self.frame_5)
        self.label_39.setObjectName(u"label_39")

        self.formLayout_6.setWidget(8, QFormLayout.LabelRole, self.label_39)

        self.tableWidget_26 = QTableWidget(self.frame_5)
        self.tableWidget_26.setObjectName(u"tableWidget_26")
        self.tableWidget_26.setEnabled(False)

        self.formLayout_6.setWidget(8, QFormLayout.FieldRole, self.tableWidget_26)

        self.label_40 = QLabel(self.frame_5)
        self.label_40.setObjectName(u"label_40")

        self.formLayout_6.setWidget(10, QFormLayout.LabelRole, self.label_40)

        self.tableWidget_27 = QTableWidget(self.frame_5)
        self.tableWidget_27.setObjectName(u"tableWidget_27")
        self.tableWidget_27.setEnabled(False)

        self.formLayout_6.setWidget(10, QFormLayout.FieldRole, self.tableWidget_27)

        self.label_41 = QLabel(self.frame_5)
        self.label_41.setObjectName(u"label_41")

        self.formLayout_6.setWidget(12, QFormLayout.LabelRole, self.label_41)

        self.tableWidget_28 = QTableWidget(self.frame_5)
        self.tableWidget_28.setObjectName(u"tableWidget_28")
        self.tableWidget_28.setEnabled(False)

        self.formLayout_6.setWidget(12, QFormLayout.FieldRole, self.tableWidget_28)

        self.label_42 = QLabel(self.frame_5)
        self.label_42.setObjectName(u"label_42")

        self.formLayout_6.setWidget(14, QFormLayout.LabelRole, self.label_42)

        self.tableWidget_29 = QTableWidget(self.frame_5)
        self.tableWidget_29.setObjectName(u"tableWidget_29")
        self.tableWidget_29.setEnabled(False)

        self.formLayout_6.setWidget(14, QFormLayout.FieldRole, self.tableWidget_29)


        self.verticalLayout_5.addWidget(self.frame_5)

        self.toolBox_4.addItem(self.page_10, u"Users and groups")
        self.page_11 = QWidget()
        self.page_11.setObjectName(u"page_11")
        self.page_11.setGeometry(QRect(0, 0, 98, 28))
        self.toolBox_4.addItem(self.page_11, u"Metadata")

        self.gridLayout.addWidget(self.toolBox_4, 0, 0, 1, 1)

        self.datasetTabProps.addWidget(self.datafileProperties)
        self.noDatasetSelectedProps = QWidget()
        self.noDatasetSelectedProps.setObjectName(u"noDatasetSelectedProps")
        self.gridLayout_8 = QGridLayout(self.noDatasetSelectedProps)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.label_43 = QLabel(self.noDatasetSelectedProps)
        self.label_43.setObjectName(u"label_43")
        sizePolicy.setHeightForWidth(self.label_43.sizePolicy().hasHeightForWidth())
        self.label_43.setSizePolicy(sizePolicy)
        self.label_43.setMinimumSize(QSize(0, 0))
        self.label_43.setMaximumSize(QSize(200, 200))
        font = QFont()
        font.setPointSize(9)
        self.label_43.setFont(font)
        self.label_43.setPixmap(QPixmap(u":/resources/noun-empty-2900960.svg"))
        self.label_43.setScaledContents(True)
        self.label_43.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_3.addWidget(self.label_43, 0, Qt.AlignHCenter)

        self.label_44 = QLabel(self.noDatasetSelectedProps)
        self.label_44.setObjectName(u"label_44")
        font1 = QFont()
        font1.setFamilies([u"Noto Sans Display"])
        font1.setPointSize(17)
        font1.setBold(True)
        self.label_44.setFont(font1)
        self.label_44.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_44)

        self.label_45 = QLabel(self.noDatasetSelectedProps)
        self.label_45.setObjectName(u"label_45")
        font2 = QFont()
        font2.setFamilies([u"Noto Sans"])
        font2.setPointSize(12)
        self.label_45.setFont(font2)
        self.label_45.setAlignment(Qt.AlignCenter)
        self.label_45.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.label_45)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)


        self.gridLayout_8.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.datasetTabProps.addWidget(self.noDatasetSelectedProps)

        self.gridLayout_2.addWidget(self.datasetTabProps, 0, 0, 1, 1)


        self.retranslateUi(DatasetProps)

        self.datasetTabProps.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(1)
        self.toolBox_4.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DatasetProps)
    # setupUi

    def retranslateUi(self, DatasetProps):
        DatasetProps.setWindowTitle(QCoreApplication.translate("DatasetProps", u"Form", None))
        self.label_21.setText(QCoreApplication.translate("DatasetProps", u"Dataset name", None))
        self.datasetNameLineEdit.setText("")
        self.datasetNameLineEdit.setPlaceholderText(QCoreApplication.translate("DatasetProps", u"The dataset name", None))
        self.label_24.setText(QCoreApplication.translate("DatasetProps", u"Instrument ID", None))
        self.instrumentIDLineEdit.setPlaceholderText(QCoreApplication.translate("DatasetProps", u"A unique identifier to the instrument that the data was generated on. Currently there is no standard persistent identifier that has widespread community adoption (DOIs are the most likely candidate).", None))
        self.label.setText(QCoreApplication.translate("DatasetProps", u"Identifiers", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QCoreApplication.translate("DatasetProps", u"General", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("DatasetProps", u"Group access", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), QCoreApplication.translate("DatasetProps", u"Metadata", None))
        self.fileInfoFilenameLabel.setText(QCoreApplication.translate("DatasetProps", u"Filename", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.fileinfoDescription), QCoreApplication.translate("DatasetProps", u"Description", None))
        self.checkBox_3.setText(QCoreApplication.translate("DatasetProps", u"Override Dataset user and group settings", None))
        self.label_36.setText(QCoreApplication.translate("DatasetProps", u"Admin groups", None))
        self.label_37.setText(QCoreApplication.translate("DatasetProps", u"Admin users", None))
        self.label_38.setText(QCoreApplication.translate("DatasetProps", u"Read groups", None))
        self.label_39.setText(QCoreApplication.translate("DatasetProps", u"Read users", None))
        self.label_40.setText(QCoreApplication.translate("DatasetProps", u"Download groups", None))
        self.label_41.setText(QCoreApplication.translate("DatasetProps", u"Download users", None))
        self.label_42.setText(QCoreApplication.translate("DatasetProps", u"Sensitive groups", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_10), QCoreApplication.translate("DatasetProps", u"Users and groups", None))
        self.toolBox_4.setItemText(self.toolBox_4.indexOf(self.page_11), QCoreApplication.translate("DatasetProps", u"Metadata", None))
        self.label_43.setText("")
        self.label_44.setText(QCoreApplication.translate("DatasetProps", u"No dataset or file selected.", None))
        self.label_45.setText(QCoreApplication.translate("DatasetProps", u"Select a dataset or file to edit metadata and access controls.", None))
    # retranslateUi

