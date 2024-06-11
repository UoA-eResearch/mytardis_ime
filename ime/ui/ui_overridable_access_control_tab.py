# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_overridable_access_control_tab.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from ime.widgets.access_control_list import AccessControlList

class Ui_OverridableAccessControlTab(object):
    def setupUi(self, OverridableAccessControlTab):
        if not OverridableAccessControlTab.objectName():
            OverridableAccessControlTab.setObjectName(u"OverridableAccessControlTab")
        OverridableAccessControlTab.resize(725, 1080)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(OverridableAccessControlTab.sizePolicy().hasHeightForWidth())
        OverridableAccessControlTab.setSizePolicy(sizePolicy)
        OverridableAccessControlTab.setMinimumSize(QSize(400, 500))
        self.verticalLayout = QVBoxLayout(OverridableAccessControlTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_5 = QLabel(OverridableAccessControlTab)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label_5.setFont(font)

        self.verticalLayout.addWidget(self.label_5)

        self.label_3 = QLabel(OverridableAccessControlTab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(OverridableAccessControlTab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_4)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(OverridableAccessControlTab)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.groupsOverride = QCheckBox(OverridableAccessControlTab)
        self.groupsOverride.setObjectName(u"groupsOverride")

        self.gridLayout.addWidget(self.groupsOverride, 0, 1, 1, 1)

        self.groups = AccessControlList(OverridableAccessControlTab)
        self.groups.setObjectName(u"groups")

        self.gridLayout.addWidget(self.groups, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(OverridableAccessControlTab)

        QMetaObject.connectSlotsByName(OverridableAccessControlTab)
    # setupUi

    def retranslateUi(self, OverridableAccessControlTab):
        OverridableAccessControlTab.setWindowTitle(QCoreApplication.translate("OverridableAccessControlTab", u"Form", None))
        self.label_5.setText(QCoreApplication.translate("OverridableAccessControlTab", u"Access Control", None))
        self.label_3.setText(QCoreApplication.translate("OverridableAccessControlTab", u"You can control the groups who can access this object. These settings apply to all data in this object, unless overridden.", None))
        self.label_4.setText(QCoreApplication.translate("OverridableAccessControlTab", u"Groups added here will have access to data in this object. You can grant additional rights like ownership, download and see sensitive metadata.", None))
        self.label.setText(QCoreApplication.translate("OverridableAccessControlTab", u"Groups", None))
        self.groupsOverride.setText(QCoreApplication.translate("OverridableAccessControlTab", u"Override", None))
    # retranslateUi

