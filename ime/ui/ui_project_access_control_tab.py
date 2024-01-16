# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_project_access_control_tab.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from ime.widgets.access_control_list import AccessControlList

class Ui_ProjectAccessControlTab(object):
    def setupUi(self, ProjectAccessControlTab):
        if not ProjectAccessControlTab.objectName():
            ProjectAccessControlTab.setObjectName(u"ProjectAccessControlTab")
        ProjectAccessControlTab.resize(725, 1080)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(ProjectAccessControlTab.sizePolicy().hasHeightForWidth())
        ProjectAccessControlTab.setSizePolicy(sizePolicy)
        ProjectAccessControlTab.setMinimumSize(QSize(400, 500))
        self.verticalLayout = QVBoxLayout(ProjectAccessControlTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_6 = QLabel(ProjectAccessControlTab)
        self.label_6.setObjectName(u"label_6")
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label_6.setFont(font)

        self.verticalLayout.addWidget(self.label_6)

        self.label_3 = QLabel(ProjectAccessControlTab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(ProjectAccessControlTab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_4)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.groups = AccessControlList(ProjectAccessControlTab)
        self.groups.setObjectName(u"groups")

        self.gridLayout.addWidget(self.groups, 0, 1, 1, 1)

        self.label = QLabel(ProjectAccessControlTab)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(ProjectAccessControlTab)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.users = AccessControlList(ProjectAccessControlTab)
        self.users.setObjectName(u"users")

        self.gridLayout.addWidget(self.users, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(ProjectAccessControlTab)

        QMetaObject.connectSlotsByName(ProjectAccessControlTab)
    # setupUi

    def retranslateUi(self, ProjectAccessControlTab):
        ProjectAccessControlTab.setWindowTitle(QCoreApplication.translate("ProjectAccessControlTab", u"Form", None))
        self.label_6.setText(QCoreApplication.translate("ProjectAccessControlTab", u"Access Control", None))
        self.label_3.setText(QCoreApplication.translate("ProjectAccessControlTab", u"You can control the users and groups who can access data in this Project. By default, the Principal Investigator is the only person who is able to access all data stored in this Project.", None))
        self.label_4.setText(QCoreApplication.translate("ProjectAccessControlTab", u"Groups and users added here will have access to data in this Project. You can grant additional rights like ownership, ability to download data and see sensitive metadata.", None))
        self.label.setText(QCoreApplication.translate("ProjectAccessControlTab", u"Groups", None))
        self.label_2.setText(QCoreApplication.translate("ProjectAccessControlTab", u"Users", None))
    # retranslateUi

