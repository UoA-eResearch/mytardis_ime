# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_identifier_list.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QListView, QPushButton,
    QSizePolicy, QWidget)

class Ui_IdentifierList(object):
    def setupUi(self, IdentifierList):
        if not IdentifierList.objectName():
            IdentifierList.setObjectName(u"IdentifierList")
        IdentifierList.resize(748, 300)
        IdentifierList.setMaximumSize(QSize(16777215, 350))
        self.gridLayout = QGridLayout(IdentifierList)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, -1, 0, -1)
        self.btnAdd = QPushButton(IdentifierList)
        self.btnAdd.setObjectName(u"btnAdd")

        self.gridLayout.addWidget(self.btnAdd, 1, 0, 1, 1)

        self.btnDelete = QPushButton(IdentifierList)
        self.btnDelete.setObjectName(u"btnDelete")

        self.gridLayout.addWidget(self.btnDelete, 1, 1, 1, 1)

        self.identifierList = QListView(IdentifierList)
        self.identifierList.setObjectName(u"identifierList")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.identifierList.sizePolicy().hasHeightForWidth())
        self.identifierList.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.identifierList, 0, 0, 1, 2)


        self.retranslateUi(IdentifierList)

        QMetaObject.connectSlotsByName(IdentifierList)
    # setupUi

    def retranslateUi(self, IdentifierList):
        IdentifierList.setWindowTitle(QCoreApplication.translate("IdentifierList", u"Form", None))
        self.btnAdd.setText(QCoreApplication.translate("IdentifierList", u"Add...", None))
        self.btnDelete.setText(QCoreApplication.translate("IdentifierList", u"Remove", None))
#if QT_CONFIG(whatsthis)
        self.identifierList.setWhatsThis(QCoreApplication.translate("IdentifierList", u"You can associate identifiers that are project-specific or externally assigned to help you distinguish the object from another, such as a RAID (Research Activity Identifier). There must be at least one identifier.", None))
#endif // QT_CONFIG(whatsthis)
    # retranslateUi

