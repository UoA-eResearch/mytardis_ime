# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_metadata_tab.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_MetadataTab(object):
    def setupUi(self, MetadataTab):
        if not MetadataTab.objectName():
            MetadataTab.setObjectName(u"MetadataTab")
        MetadataTab.resize(766, 639)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MetadataTab.sizePolicy().hasHeightForWidth())
        MetadataTab.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(MetadataTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(MetadataTab)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        self.label_3.setFont(font)

        self.verticalLayout.addWidget(self.label_3)

        self.label = QLabel(MetadataTab)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.schemaLabel = QLabel(MetadataTab)
        self.schemaLabel.setObjectName(u"schemaLabel")

        self.horizontalLayout.addWidget(self.schemaLabel)

        self.schemaLineEdit = QLineEdit(MetadataTab)
        self.schemaLineEdit.setObjectName(u"schemaLineEdit")

        self.horizontalLayout.addWidget(self.schemaLineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.widget = QWidget(MetadataTab)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout.addWidget(self.widget)

        self.metadata_table = QTableWidget(MetadataTab)
        if (self.metadata_table.columnCount() < 2):
            self.metadata_table.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.metadata_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.metadata_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.metadata_table.setObjectName(u"metadata_table")
        self.metadata_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.metadata_table.horizontalHeader().setStretchLastSection(True)
        self.metadata_table.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.metadata_table)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.add_row_btn = QPushButton(MetadataTab)
        self.add_row_btn.setObjectName(u"add_row_btn")

        self.horizontalLayout_3.addWidget(self.add_row_btn)

        self.remove_rows_btn = QPushButton(MetadataTab)
        self.remove_rows_btn.setObjectName(u"remove_rows_btn")
        self.remove_rows_btn.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.remove_rows_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.label_2 = QLabel(MetadataTab)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.label_2.setFont(font1)

        self.verticalLayout.addWidget(self.label_2)

        self.label_4 = QLabel(MetadataTab)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.notes_textedit = QTextEdit(MetadataTab)
        self.notes_textedit.setObjectName(u"notes_textedit")

        self.verticalLayout.addWidget(self.notes_textedit)


        self.retranslateUi(MetadataTab)

        QMetaObject.connectSlotsByName(MetadataTab)
    # setupUi

    def retranslateUi(self, MetadataTab):
        MetadataTab.setWindowTitle(QCoreApplication.translate("MetadataTab", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("MetadataTab", u"Metadata", None))
        self.label.setText(QCoreApplication.translate("MetadataTab", u"You can add metadata to help you and your collaborators remember the conditions in which the data was produced. You can also create schemas in MyTardis that specify standard fields to fill in.", None))
        self.schemaLabel.setText(QCoreApplication.translate("MetadataTab", u"Schema", None))
        ___qtablewidgetitem = self.metadata_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MetadataTab", u"Metadata name", None));
        ___qtablewidgetitem1 = self.metadata_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MetadataTab", u"Value", None));
        self.add_row_btn.setText(QCoreApplication.translate("MetadataTab", u"Add...", None))
        self.remove_rows_btn.setText(QCoreApplication.translate("MetadataTab", u"Remove", None))
        self.label_2.setText(QCoreApplication.translate("MetadataTab", u"Notes", None))
        self.label_4.setText(QCoreApplication.translate("MetadataTab", u"Add notes for recording unstructured observations.", None))
    # retranslateUi

