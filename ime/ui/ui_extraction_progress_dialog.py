# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_extraction_progress_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QProgressBar, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_ExtractionProgressDialog(object):
    def setupUi(self, ExtractionProgressDialog):
        if not ExtractionProgressDialog.objectName():
            ExtractionProgressDialog.setObjectName(u"ExtractionProgressDialog")
        ExtractionProgressDialog.resize(518, 112)
        ExtractionProgressDialog.setModal(True)
        self.gridLayout = QGridLayout(ExtractionProgressDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ExtractionProgressDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(ExtractionProgressDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)

        self.fileName = QLabel(ExtractionProgressDialog)
        self.fileName.setObjectName(u"fileName")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileName.sizePolicy().hasHeightForWidth())
        self.fileName.setSizePolicy(sizePolicy)
        self.fileName.setWordWrap(True)

        self.verticalLayout.addWidget(self.fileName)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(ExtractionProgressDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)


        self.retranslateUi(ExtractionProgressDialog)
        self.buttonBox.accepted.connect(ExtractionProgressDialog.accept)
        self.buttonBox.rejected.connect(ExtractionProgressDialog.reject)

        QMetaObject.connectSlotsByName(ExtractionProgressDialog)
    # setupUi

    def retranslateUi(self, ExtractionProgressDialog):
        ExtractionProgressDialog.setWindowTitle(QCoreApplication.translate("ExtractionProgressDialog", u"Finishing data file import", None))
        self.label.setText(QCoreApplication.translate("ExtractionProgressDialog", u"Extracting metadata from images...", None))
        self.fileName.setText("")
    # retranslateUi

