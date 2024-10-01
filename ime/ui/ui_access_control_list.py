# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_access_control_list.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLayout, QPushButton, QSizePolicy, QSpacerItem,
    QTableView, QVBoxLayout, QWidget)

class Ui_AccessControlList(object):
    def setupUi(self, AccessControlList):
        if not AccessControlList.objectName():
            AccessControlList.setObjectName(u"AccessControlList")
        AccessControlList.resize(555, 290)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(AccessControlList.sizePolicy().hasHeightForWidth())
        AccessControlList.setSizePolicy(sizePolicy)
        AccessControlList.setMinimumSize(QSize(0, 150))
        self.gridLayout = QGridLayout(AccessControlList)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(6)
        self.gridLayout.setContentsMargins(-1, -1, -1, 9)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.aclTable = QTableView(AccessControlList)
        self.aclTable.setObjectName(u"aclTable")

        self.horizontalLayout_2.addWidget(self.aclTable)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.btnAdd = QPushButton(AccessControlList)
        self.btnAdd.setObjectName(u"btnAdd")

        self.verticalLayout_2.addWidget(self.btnAdd)

        self.btnDelete = QPushButton(AccessControlList)
        self.btnDelete.setObjectName(u"btnDelete")

        self.verticalLayout_2.addWidget(self.btnDelete)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)


        self.retranslateUi(AccessControlList)

        QMetaObject.connectSlotsByName(AccessControlList)
    # setupUi

    def retranslateUi(self, AccessControlList):
        AccessControlList.setWindowTitle(QCoreApplication.translate("AccessControlList", u"Form", None))
        self.btnAdd.setText(QCoreApplication.translate("AccessControlList", u"Add", None))
        self.btnDelete.setText(QCoreApplication.translate("AccessControlList", u"Remove", None))
    # retranslateUi

