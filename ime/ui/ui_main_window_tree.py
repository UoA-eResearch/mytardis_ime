# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_window_tree.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QSizePolicy, QSpacerItem,
    QStackedWidget, QTabWidget, QToolBar, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

from ime.widgets.prop_editor import ProjectPropertyEditor
import default_rc
import default_rc
import default_rc
import default_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1183, 505)
        self.actionNewFile = QAction(MainWindow)
        self.actionNewFile.setObjectName(u"actionNewFile")
        self.actionFrom_a_template = QAction(MainWindow)
        self.actionFrom_a_template.setObjectName(u"actionFrom_a_template")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_as_template = QAction(MainWindow)
        self.actionSave_as_template.setObjectName(u"actionSave_as_template")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionImport_data_files = QAction(MainWindow)
        self.actionImport_data_files.setObjectName(u"actionImport_data_files")
        icon = QIcon()
        icon.addFile(u":/resources/noun-file-add-4877075.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionImport_data_files.setIcon(icon)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.editorTabs = QTabWidget(self.centralwidget)
        self.editorTabs.setObjectName(u"editorTabs")
        self.project_tab = QWidget()
        self.project_tab.setObjectName(u"project_tab")
        self.horizontalLayout_3 = QHBoxLayout(self.project_tab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.projectTreeWidget = QTreeWidget(self.project_tab)
        __qtreewidgetitem = QTreeWidgetItem(self.projectTreeWidget)
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem2 = QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem2)
        __qtreewidgetitem3 = QTreeWidgetItem(__qtreewidgetitem)
        __qtreewidgetitem4 = QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem4)
        QTreeWidgetItem(__qtreewidgetitem3)
        __qtreewidgetitem5 = QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem5)
        QTreeWidgetItem(__qtreewidgetitem5)
        __qtreewidgetitem6 = QTreeWidgetItem(self.projectTreeWidget)
        __qtreewidgetitem7 = QTreeWidgetItem(__qtreewidgetitem6)
        __qtreewidgetitem8 = QTreeWidgetItem(__qtreewidgetitem7)
        QTreeWidgetItem(__qtreewidgetitem8)
        self.projectTreeWidget.setObjectName(u"projectTreeWidget")

        self.horizontalLayout_3.addWidget(self.projectTreeWidget)

        self.projectTabProps = QStackedWidget(self.project_tab)
        self.projectTabProps.setObjectName(u"projectTabProps")
        self.projectProperties = ProjectPropertyEditor()
        self.projectProperties.setObjectName(u"projectProperties")
        self.gridLayout_11 = QGridLayout(self.projectProperties)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.projectTabProps.addWidget(self.projectProperties)
        self.page_15 = QWidget()
        self.page_15.setObjectName(u"page_15")
        self.gridLayout_12 = QGridLayout(self.page_15)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_7)

        self.label_52 = QLabel(self.page_15)
        self.label_52.setObjectName(u"label_52")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_52.sizePolicy().hasHeightForWidth())
        self.label_52.setSizePolicy(sizePolicy)
        self.label_52.setMinimumSize(QSize(0, 0))
        self.label_52.setMaximumSize(QSize(200, 200))
        font = QFont()
        font.setPointSize(9)
        self.label_52.setFont(font)
        self.label_52.setPixmap(QPixmap(u":/resources/noun-empty-2900960.svg"))
        self.label_52.setScaledContents(True)
        self.label_52.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_8.addWidget(self.label_52, 0, Qt.AlignHCenter)

        self.label_53 = QLabel(self.page_15)
        self.label_53.setObjectName(u"label_53")
        font1 = QFont()
        font1.setFamilies([u"Noto Sans Display"])
        font1.setPointSize(17)
        font1.setBold(True)
        self.label_53.setFont(font1)
        self.label_53.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_53)

        self.label_54 = QLabel(self.page_15)
        self.label_54.setObjectName(u"label_54")
        font2 = QFont()
        font2.setFamilies([u"Noto Sans"])
        font2.setPointSize(12)
        self.label_54.setFont(font2)
        self.label_54.setAlignment(Qt.AlignCenter)
        self.label_54.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.label_54)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_8)


        self.gridLayout_12.addLayout(self.verticalLayout_8, 0, 0, 1, 1)

        self.projectTabProps.addWidget(self.page_15)

        self.horizontalLayout_3.addWidget(self.projectTabProps)

        self.editorTabs.addTab(self.project_tab, "")

        self.verticalLayout_2.addWidget(self.editorTabs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionNewFile)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionImport_data_files)

        self.retranslateUi(MainWindow)

        self.editorTabs.setCurrentIndex(0)
        self.projectTabProps.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MyTardis Ingestion Editor", None))
        self.actionNewFile.setText(QCoreApplication.translate("MainWindow", u"New...", None))
#if QT_CONFIG(tooltip)
        self.actionNewFile.setToolTip(QCoreApplication.translate("MainWindow", u"Create a new metadata file", None))
#endif // QT_CONFIG(tooltip)
        self.actionFrom_a_template.setText(QCoreApplication.translate("MainWindow", u"From a template...", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_as_template.setText(QCoreApplication.translate("MainWindow", u"Save as template", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionImport_data_files.setText(QCoreApplication.translate("MainWindow", u"Import data files", None))
#if QT_CONFIG(tooltip)
        self.actionImport_data_files.setToolTip(QCoreApplication.translate("MainWindow", u"Launch guide to import new data files", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionImport_data_files.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+I", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(QCoreApplication.translate("MainWindow", u"Open", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        ___qtreewidgetitem = self.projectTreeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Size", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Name", None));

        __sortingEnabled = self.projectTreeWidget.isSortingEnabled()
        self.projectTreeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.projectTreeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Breast Cancer Drug Treatment Genomics", None));
        ___qtreewidgetitem2 = ___qtreewidgetitem1.child(0)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"No treatment", None));
        ___qtreewidgetitem3 = ___qtreewidgetitem2.child(0)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"Raw", None));
        ___qtreewidgetitem4 = ___qtreewidgetitem3.child(0)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"file1.txt", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem3.child(1)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"file2.txt", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem1.child(1)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"Herceptin", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem6.child(0)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("MainWindow", u"Raw", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem7.child(0)
        ___qtreewidgetitem8.setText(1, QCoreApplication.translate("MainWindow", u"file3.txt", None));
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("MainWindow", u"New Subitem", None));
        ___qtreewidgetitem9 = ___qtreewidgetitem6.child(1)
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("MainWindow", u"Aligned", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem1.child(2)
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("MainWindow", u"Keytruda", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem10.child(0)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("MainWindow", u"Raw", None));
        ___qtreewidgetitem12 = ___qtreewidgetitem10.child(1)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("MainWindow", u"Aligned", None));
        ___qtreewidgetitem13 = self.projectTreeWidget.topLevelItem(1)
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("MainWindow", u"P2", None));
        ___qtreewidgetitem14 = ___qtreewidgetitem13.child(0)
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("MainWindow", u"E3", None));
        ___qtreewidgetitem15 = ___qtreewidgetitem14.child(0)
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("MainWindow", u"D3", None));
        ___qtreewidgetitem16 = ___qtreewidgetitem15.child(0)
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("MainWindow", u"file4.txt", None));
        self.projectTreeWidget.setSortingEnabled(__sortingEnabled)

        self.label_52.setText("")
        self.label_53.setText(QCoreApplication.translate("MainWindow", u"No project selected.", None))
        self.label_54.setText(QCoreApplication.translate("MainWindow", u"Select a project to edit metadata and access control properties.", None))
        self.editorTabs.setTabText(self.editorTabs.indexOf(self.project_tab), QCoreApplication.translate("MainWindow", u"Projects", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

