# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
    QSplitter, QStackedWidget, QTabWidget, QToolBar,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

from ime.widgets.prop_editor import (DatafilePropertyEditor, DatasetPropertyEditor, ExperimentPropertyEditor, ProjectPropertyEditor)
import default_rc
import default_rc
import default_rc
import default_rc
import default_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1319, 650)
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
        self.gridLayout = QGridLayout(self.project_tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter_2 = QSplitter(self.project_tab)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.splitter_2.setChildrenCollapsible(False)
        self.projectTreeWidget = QTreeWidget(self.splitter_2)
        self.projectTreeWidget.setObjectName(u"projectTreeWidget")
        self.projectTreeWidget.setMinimumSize(QSize(600, 0))
        self.projectTreeWidget.setBaseSize(QSize(600, 0))
        self.splitter_2.addWidget(self.projectTreeWidget)
        self.projectTabProps = QStackedWidget(self.splitter_2)
        self.projectTabProps.setObjectName(u"projectTabProps")
        self.projectTabProps.setMinimumSize(QSize(500, 0))
        self.projectTabProps.setBaseSize(QSize(500, 0))
        self.projectProperties = ProjectPropertyEditor()
        self.projectProperties.setObjectName(u"projectProperties")
        self.gridLayout_13 = QGridLayout(self.projectProperties)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.projectTabProps.addWidget(self.projectProperties)
        self.page_16 = QWidget()
        self.page_16.setObjectName(u"page_16")
        self.page_16.setMinimumSize(QSize(500, 0))
        self.page_16.setBaseSize(QSize(500, 0))
        self.horizontalLayout = QHBoxLayout(self.page_16)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_9)

        self.label_55 = QLabel(self.page_16)
        self.label_55.setObjectName(u"label_55")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_55.sizePolicy().hasHeightForWidth())
        self.label_55.setSizePolicy(sizePolicy)
        self.label_55.setMinimumSize(QSize(0, 0))
        self.label_55.setMaximumSize(QSize(200, 200))
        font = QFont()
        font.setPointSize(9)
        self.label_55.setFont(font)
        self.label_55.setPixmap(QPixmap(u":/resources/noun-empty-2900960.svg"))
        self.label_55.setScaledContents(True)
        self.label_55.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_9.addWidget(self.label_55, 0, Qt.AlignHCenter)

        self.label_56 = QLabel(self.page_16)
        self.label_56.setObjectName(u"label_56")
        font1 = QFont()
        font1.setFamilies([u"Noto Sans Display"])
        font1.setPointSize(17)
        font1.setBold(True)
        self.label_56.setFont(font1)
        self.label_56.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_56)

        self.label_57 = QLabel(self.page_16)
        self.label_57.setObjectName(u"label_57")
        font2 = QFont()
        font2.setFamilies([u"Noto Sans"])
        font2.setPointSize(12)
        self.label_57.setFont(font2)
        self.label_57.setAlignment(Qt.AlignCenter)
        self.label_57.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.label_57)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_10)


        self.horizontalLayout.addLayout(self.verticalLayout_9)

        self.projectTabProps.addWidget(self.page_16)
        self.splitter_2.addWidget(self.projectTabProps)

        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)

        self.editorTabs.addTab(self.project_tab, "")
        self.experiment_tab = QWidget()
        self.experiment_tab.setObjectName(u"experiment_tab")
        self.gridLayout_3 = QGridLayout(self.experiment_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.splitter_3 = QSplitter(self.experiment_tab)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.splitter_3.setChildrenCollapsible(False)
        self.experimentTreeWidget = QTreeWidget(self.splitter_3)
        self.experimentTreeWidget.setObjectName(u"experimentTreeWidget")
        self.experimentTreeWidget.setMinimumSize(QSize(600, 0))
        self.experimentTreeWidget.setBaseSize(QSize(600, 0))
        self.splitter_3.addWidget(self.experimentTreeWidget)
        self.experimentTabProps = QStackedWidget(self.splitter_3)
        self.experimentTabProps.setObjectName(u"experimentTabProps")
        self.experimentTabProps.setMinimumSize(QSize(500, 0))
        self.experimentTabProps.setBaseSize(QSize(500, 0))
        self.expProperties = ExperimentPropertyEditor()
        self.expProperties.setObjectName(u"expProperties")
        self.gridLayout_9 = QGridLayout(self.expProperties)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.experimentTabProps.addWidget(self.expProperties)
        self.page_13 = QWidget()
        self.page_13.setObjectName(u"page_13")
        self.page_13.setMinimumSize(QSize(500, 0))
        self.page_13.setBaseSize(QSize(500, 0))
        self.gridLayout_4 = QGridLayout(self.page_13)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.label_46 = QLabel(self.page_13)
        self.label_46.setObjectName(u"label_46")
        sizePolicy.setHeightForWidth(self.label_46.sizePolicy().hasHeightForWidth())
        self.label_46.setSizePolicy(sizePolicy)
        self.label_46.setMinimumSize(QSize(0, 0))
        self.label_46.setMaximumSize(QSize(200, 200))
        self.label_46.setFont(font)
        self.label_46.setPixmap(QPixmap(u":/resources/noun-empty-2900960.svg"))
        self.label_46.setScaledContents(True)
        self.label_46.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.verticalLayout_6.addWidget(self.label_46, 0, Qt.AlignHCenter)

        self.label_47 = QLabel(self.page_13)
        self.label_47.setObjectName(u"label_47")
        self.label_47.setFont(font1)
        self.label_47.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_47)

        self.label_48 = QLabel(self.page_13)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setFont(font2)
        self.label_48.setAlignment(Qt.AlignCenter)
        self.label_48.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.label_48)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)


        self.gridLayout_4.addLayout(self.verticalLayout_6, 0, 0, 1, 1)

        self.experimentTabProps.addWidget(self.page_13)
        self.splitter_3.addWidget(self.experimentTabProps)

        self.gridLayout_3.addWidget(self.splitter_3, 0, 0, 1, 1)

        self.editorTabs.addTab(self.experiment_tab, "")
        self.dataset_tab = QWidget()
        self.dataset_tab.setObjectName(u"dataset_tab")
        self.horizontalLayout_2 = QHBoxLayout(self.dataset_tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.splitter = QSplitter(self.dataset_tab)
        self.splitter.setObjectName(u"splitter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy1)
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.datasetTreeWidget = QTreeWidget(self.splitter)
        self.datasetTreeWidget.setObjectName(u"datasetTreeWidget")
        sizePolicy1.setHeightForWidth(self.datasetTreeWidget.sizePolicy().hasHeightForWidth())
        self.datasetTreeWidget.setSizePolicy(sizePolicy1)
        self.datasetTreeWidget.setMinimumSize(QSize(600, 0))
        self.datasetTreeWidget.setBaseSize(QSize(600, 0))
        self.splitter.addWidget(self.datasetTreeWidget)
        self.datasetTabProps = QStackedWidget(self.splitter)
        self.datasetTabProps.setObjectName(u"datasetTabProps")
        sizePolicy1.setHeightForWidth(self.datasetTabProps.sizePolicy().hasHeightForWidth())
        self.datasetTabProps.setSizePolicy(sizePolicy1)
        self.datasetTabProps.setMinimumSize(QSize(500, 0))
        self.datasetTabProps.setBaseSize(QSize(600, 0))
        self.datasetProperties = DatasetPropertyEditor()
        self.datasetProperties.setObjectName(u"datasetProperties")
        self.gridLayout_7 = QGridLayout(self.datasetProperties)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.datasetTabProps.addWidget(self.datasetProperties)
        self.datafileProperties = DatafilePropertyEditor()
        self.datafileProperties.setObjectName(u"datafileProperties")
        self.gridLayout_2 = QGridLayout(self.datafileProperties)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.datasetTabProps.addWidget(self.datafileProperties)
        self.noDatasetSelectedProps = QWidget()
        self.noDatasetSelectedProps.setObjectName(u"noDatasetSelectedProps")
        sizePolicy1.setHeightForWidth(self.noDatasetSelectedProps.sizePolicy().hasHeightForWidth())
        self.noDatasetSelectedProps.setSizePolicy(sizePolicy1)
        self.noDatasetSelectedProps.setMinimumSize(QSize(500, 0))
        self.noDatasetSelectedProps.setBaseSize(QSize(500, 0))
        self.verticalLayout = QVBoxLayout(self.noDatasetSelectedProps)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_5)

        self.label_49 = QLabel(self.noDatasetSelectedProps)
        self.label_49.setObjectName(u"label_49")
        sizePolicy.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy)
        self.label_49.setMinimumSize(QSize(0, 0))
        self.label_49.setMaximumSize(QSize(200, 200))
        self.label_49.setFont(font)
        self.label_49.setPixmap(QPixmap(u":/resources/noun-empty-2900960.svg"))
        self.label_49.setScaledContents(True)
        self.label_49.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_49, 0, Qt.AlignHCenter)

        self.label_50 = QLabel(self.noDatasetSelectedProps)
        self.label_50.setObjectName(u"label_50")
        self.label_50.setFont(font1)
        self.label_50.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_50, 0, Qt.AlignHCenter)

        self.label_51 = QLabel(self.noDatasetSelectedProps)
        self.label_51.setObjectName(u"label_51")
        self.label_51.setFont(font2)
        self.label_51.setAlignment(Qt.AlignCenter)
        self.label_51.setWordWrap(False)

        self.verticalLayout_4.addWidget(self.label_51, 0, Qt.AlignHCenter)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_6)


        self.verticalLayout.addLayout(self.verticalLayout_4)

        self.datasetTabProps.addWidget(self.noDatasetSelectedProps)
        self.splitter.addWidget(self.datasetTabProps)

        self.horizontalLayout_2.addWidget(self.splitter)

        self.editorTabs.addTab(self.dataset_tab, "")

        self.verticalLayout_2.addWidget(self.editorTabs)

        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionImport_data_files)

        self.retranslateUi(MainWindow)

        self.editorTabs.setCurrentIndex(0)
        self.projectTabProps.setCurrentIndex(1)
        self.experimentTabProps.setCurrentIndex(1)
        self.datasetTabProps.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Instrument Data Wizard", None))
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
        self.label_55.setText("")
        self.label_56.setText(QCoreApplication.translate("MainWindow", u"No project selected.", None))
        self.label_57.setText(QCoreApplication.translate("MainWindow", u"Select a project to edit metadata and access control properties.", None))
        self.editorTabs.setTabText(self.editorTabs.indexOf(self.project_tab), QCoreApplication.translate("MainWindow", u"Projects", None))
        ___qtreewidgetitem1 = self.experimentTreeWidget.headerItem()
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("MainWindow", u"Linked project", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("MainWindow", u"Size", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Name", None));
        self.label_46.setText("")
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"No experiment selected.", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"Select an experiment to edit metadata and access control properties.", None))
        self.editorTabs.setTabText(self.editorTabs.indexOf(self.experiment_tab), QCoreApplication.translate("MainWindow", u"Experiments", None))
        ___qtreewidgetitem2 = self.datasetTreeWidget.headerItem()
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("MainWindow", u"Linked experiment", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("MainWindow", u"Size", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"Name", None));
        self.label_49.setText("")
        self.label_50.setText(QCoreApplication.translate("MainWindow", u"No dataset or file selected.", None))
        self.label_51.setText(QCoreApplication.translate("MainWindow", u"Select a dataset or file to edit metadata and access controls.", None))
        self.editorTabs.setTabText(self.editorTabs.indexOf(self.dataset_tab), QCoreApplication.translate("MainWindow", u"Datasets", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

