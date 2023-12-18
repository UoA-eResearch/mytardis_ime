# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_add_files_wizard.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
    QWizard, QWizardPage)

from ime.widgets.add_files_wizard.dataset_page import DatasetPage
from ime.widgets.add_files_wizard.experiment_page import ExperimentPage
from ime.widgets.add_files_wizard.included_files_page import IncludedFilesPage
from ime.widgets.add_files_wizard.project_page import ProjectPage
from ime.widgets.add_files_wizard.skip_dataset_intro_page import SkipDatasetIntroPage
from ime.widgets.add_files_wizard.skip_experiment_intro_page import SkipExperimentIntroPage
from ime.widgets.add_files_wizard.skip_project_intro_page import SkipProjectIntroPage
import default_rc
import default_rc
import default_rc
import default_rc

class Ui_ImportDataFiles(object):
    def setupUi(self, ImportDataFiles):
        if not ImportDataFiles.objectName():
            ImportDataFiles.setObjectName(u"ImportDataFiles")
        ImportDataFiles.resize(863, 510)
        self.introductionPage = QWizardPage()
        self.introductionPage.setObjectName(u"introductionPage")
        self.gridLayout_4 = QGridLayout(self.introductionPage)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_14 = QLabel(self.introductionPage)
        self.label_14.setObjectName(u"label_14")
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        self.label_14.setFont(font)

        self.verticalLayout.addWidget(self.label_14)

        self.label_9 = QLabel(self.introductionPage)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_9)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.mytardisdatamodelexplanation = QFrame(self.introductionPage)
        self.mytardisdatamodelexplanation.setObjectName(u"mytardisdatamodelexplanation")
        self.mytardisdatamodelexplanation.setMinimumSize(QSize(0, 310))
        self.horizontalLayout_3 = QHBoxLayout(self.mytardisdatamodelexplanation)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_12 = QLabel(self.mytardisdatamodelexplanation)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(0, 253))
        self.label_12.setMaximumSize(QSize(300, 16777215))
        self.label_12.setPixmap(QPixmap(u":/resources/text66-1-7.png"))
        self.label_12.setMargin(0)

        self.horizontalLayout_3.addWidget(self.label_12)

        self.label_10 = QLabel(self.mytardisdatamodelexplanation)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setWordWrap(True)
        self.label_10.setMargin(0)

        self.horizontalLayout_3.addWidget(self.label_10)


        self.verticalLayout.addWidget(self.mytardisdatamodelexplanation)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.label_11 = QLabel(self.introductionPage)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_11)


        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)

        ImportDataFiles.setPage(0, self.introductionPage)
        self.projectPage = ProjectPage()
        self.projectPage.setObjectName(u"projectPage")
        self.verticalLayout_2 = QVBoxLayout(self.projectPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.projectPage)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.verticalLayout_2.addWidget(self.label_4)

        self.label = QLabel(self.projectPage)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.existingProjectRadioButton = QRadioButton(self.projectPage)
        self.existingProjectRadioButton.setObjectName(u"existingProjectRadioButton")
        self.existingProjectRadioButton.setEnabled(True)
        self.existingProjectRadioButton.setCheckable(True)
        self.existingProjectRadioButton.setChecked(True)

        self.verticalLayout_2.addWidget(self.existingProjectRadioButton)

        self.existingProjectForm = QWidget(self.projectPage)
        self.existingProjectForm.setObjectName(u"existingProjectForm")
        self.gridLayout_9 = QGridLayout(self.existingProjectForm)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.existingProjectList = QComboBox(self.existingProjectForm)
        self.existingProjectList.setObjectName(u"existingProjectList")

        self.gridLayout_9.addWidget(self.existingProjectList, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.existingProjectForm)

        self.newProjectRadioButton = QRadioButton(self.projectPage)
        self.newProjectRadioButton.setObjectName(u"newProjectRadioButton")
        self.newProjectRadioButton.setChecked(False)

        self.verticalLayout_2.addWidget(self.newProjectRadioButton)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        ImportDataFiles.setPage(2, self.projectPage)
        self.newProjectPage = QWizardPage()
        self.newProjectPage.setObjectName(u"newProjectPage")
        self.gridLayout_10 = QGridLayout(self.newProjectPage)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_13 = QLabel(self.newProjectPage)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_10.addWidget(self.label_13, 1, 0, 1, 1)

        self.newProjectForm = QWidget(self.newProjectPage)
        self.newProjectForm.setObjectName(u"newProjectForm")
        self._3 = QFormLayout(self.newProjectForm)
        self._3.setObjectName(u"_3")
        self.projectNameLabel = QLabel(self.newProjectForm)
        self.projectNameLabel.setObjectName(u"projectNameLabel")

        self._3.setWidget(0, QFormLayout.LabelRole, self.projectNameLabel)

        self.projectNameLineEdit = QLineEdit(self.newProjectForm)
        self.projectNameLineEdit.setObjectName(u"projectNameLineEdit")

        self._3.setWidget(0, QFormLayout.FieldRole, self.projectNameLineEdit)

        self.projectIDLabel = QLabel(self.newProjectForm)
        self.projectIDLabel.setObjectName(u"projectIDLabel")

        self._3.setWidget(2, QFormLayout.LabelRole, self.projectIDLabel)

        self.projectIDLineEdit = QLineEdit(self.newProjectForm)
        self.projectIDLineEdit.setObjectName(u"projectIDLineEdit")

        self._3.setWidget(2, QFormLayout.FieldRole, self.projectIDLineEdit)

        self.label_24 = QLabel(self.newProjectForm)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setOpenExternalLinks(True)

        self._3.setWidget(3, QFormLayout.FieldRole, self.label_24)

        self.projectDescriptionLabel = QLabel(self.newProjectForm)
        self.projectDescriptionLabel.setObjectName(u"projectDescriptionLabel")

        self._3.setWidget(5, QFormLayout.LabelRole, self.projectDescriptionLabel)

        self.piLabel = QLabel(self.newProjectForm)
        self.piLabel.setObjectName(u"piLabel")

        self._3.setWidget(4, QFormLayout.LabelRole, self.piLabel)

        self.piLineEdit = QLineEdit(self.newProjectForm)
        self.piLineEdit.setObjectName(u"piLineEdit")

        self._3.setWidget(4, QFormLayout.FieldRole, self.piLineEdit)

        self.projectDescriptionTextEdit = QTextEdit(self.newProjectForm)
        self.projectDescriptionTextEdit.setObjectName(u"projectDescriptionTextEdit")

        self._3.setWidget(5, QFormLayout.FieldRole, self.projectDescriptionTextEdit)


        self.gridLayout_10.addWidget(self.newProjectForm, 2, 0, 1, 1)

        self.label_15 = QLabel(self.newProjectPage)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_10.addWidget(self.label_15, 3, 0, 1, 1)

        self.label_2 = QLabel(self.newProjectPage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout_10.addWidget(self.label_2, 0, 0, 1, 1)

        ImportDataFiles.setPage(10, self.newProjectPage)
        self.experimentPage = ExperimentPage()
        self.experimentPage.setObjectName(u"experimentPage")
        self.verticalLayout_3 = QVBoxLayout(self.experimentPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_18 = QLabel(self.experimentPage)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font)

        self.verticalLayout_3.addWidget(self.label_18)

        self.label_3 = QLabel(self.experimentPage)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.existingExperimentRadioButton = QRadioButton(self.experimentPage)
        self.existingExperimentRadioButton.setObjectName(u"existingExperimentRadioButton")
        self.existingExperimentRadioButton.setEnabled(True)
        self.existingExperimentRadioButton.setChecked(True)

        self.verticalLayout_3.addWidget(self.existingExperimentRadioButton)

        self.existingProjectForm_2 = QWidget(self.experimentPage)
        self.existingProjectForm_2.setObjectName(u"existingProjectForm_2")
        self.gridLayout_7 = QGridLayout(self.existingProjectForm_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.existingExperimentList = QComboBox(self.existingProjectForm_2)
        self.existingExperimentList.setObjectName(u"existingExperimentList")

        self.gridLayout_7.addWidget(self.existingExperimentList, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.existingProjectForm_2)

        self.newExperimentRadioButton = QRadioButton(self.experimentPage)
        self.newExperimentRadioButton.setObjectName(u"newExperimentRadioButton")
        self.newExperimentRadioButton.setChecked(False)

        self.verticalLayout_3.addWidget(self.newExperimentRadioButton)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        ImportDataFiles.setPage(4, self.experimentPage)
        self.newExperimentPage = QWizardPage()
        self.newExperimentPage.setObjectName(u"newExperimentPage")
        self.verticalLayout_6 = QVBoxLayout(self.newExperimentPage)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_20 = QLabel(self.newExperimentPage)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font)

        self.verticalLayout_6.addWidget(self.label_20)

        self.label_16 = QLabel(self.newExperimentPage)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout_6.addWidget(self.label_16)

        self.newExperimentForm = QWidget(self.newExperimentPage)
        self.newExperimentForm.setObjectName(u"newExperimentForm")
        self._2 = QFormLayout(self.newExperimentForm)
        self._2.setObjectName(u"_2")
        self.experimentNameLabel = QLabel(self.newExperimentForm)
        self.experimentNameLabel.setObjectName(u"experimentNameLabel")

        self._2.setWidget(0, QFormLayout.LabelRole, self.experimentNameLabel)

        self.experimentNameLineEdit = QLineEdit(self.newExperimentForm)
        self.experimentNameLineEdit.setObjectName(u"experimentNameLineEdit")

        self._2.setWidget(0, QFormLayout.FieldRole, self.experimentNameLineEdit)

        self.experimentIDLabel = QLabel(self.newExperimentForm)
        self.experimentIDLabel.setObjectName(u"experimentIDLabel")

        self._2.setWidget(1, QFormLayout.LabelRole, self.experimentIDLabel)

        self.experimentIDLineEdit = QLineEdit(self.newExperimentForm)
        self.experimentIDLineEdit.setObjectName(u"experimentIDLineEdit")

        self._2.setWidget(1, QFormLayout.FieldRole, self.experimentIDLineEdit)

        self.label_25 = QLabel(self.newExperimentForm)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setOpenExternalLinks(True)

        self._2.setWidget(2, QFormLayout.FieldRole, self.label_25)

        self.experimentdescriptionLabel = QLabel(self.newExperimentForm)
        self.experimentdescriptionLabel.setObjectName(u"experimentdescriptionLabel")

        self._2.setWidget(3, QFormLayout.LabelRole, self.experimentdescriptionLabel)

        self.experimentDescriptionLineEdit = QTextEdit(self.newExperimentForm)
        self.experimentDescriptionLineEdit.setObjectName(u"experimentDescriptionLineEdit")

        self._2.setWidget(3, QFormLayout.FieldRole, self.experimentDescriptionLineEdit)


        self.verticalLayout_6.addWidget(self.newExperimentForm)

        self.label_17 = QLabel(self.newExperimentPage)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_6.addWidget(self.label_17)

        ImportDataFiles.setPage(11, self.newExperimentPage)
        self.datasetPage = DatasetPage()
        self.datasetPage.setObjectName(u"datasetPage")
        self.verticalLayout_4 = QVBoxLayout(self.datasetPage)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_21 = QLabel(self.datasetPage)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font)

        self.verticalLayout_4.addWidget(self.label_21)

        self.label_5 = QLabel(self.datasetPage)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_4.addWidget(self.label_5)

        self.existingDatasetRadioButton = QRadioButton(self.datasetPage)
        self.existingDatasetRadioButton.setObjectName(u"existingDatasetRadioButton")
        self.existingDatasetRadioButton.setEnabled(True)
        self.existingDatasetRadioButton.setChecked(False)

        self.verticalLayout_4.addWidget(self.existingDatasetRadioButton)

        self.existingDatasetForm = QWidget(self.datasetPage)
        self.existingDatasetForm.setObjectName(u"existingDatasetForm")
        self.gridLayout_12 = QGridLayout(self.existingDatasetForm)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.existingDatasetList = QComboBox(self.existingDatasetForm)
        self.existingDatasetList.setObjectName(u"existingDatasetList")

        self.gridLayout_12.addWidget(self.existingDatasetList, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.existingDatasetForm)

        self.newDatasetRadioButton = QRadioButton(self.datasetPage)
        self.newDatasetRadioButton.setObjectName(u"newDatasetRadioButton")
        self.newDatasetRadioButton.setChecked(True)

        self.verticalLayout_4.addWidget(self.newDatasetRadioButton)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_5)

        ImportDataFiles.setPage(6, self.datasetPage)
        self.newDatasetPage = QWizardPage()
        self.newDatasetPage.setObjectName(u"newDatasetPage")
        self.verticalLayout_8 = QVBoxLayout(self.newDatasetPage)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_22 = QLabel(self.newDatasetPage)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font)

        self.verticalLayout_8.addWidget(self.label_22)

        self.label_19 = QLabel(self.newDatasetPage)
        self.label_19.setObjectName(u"label_19")

        self.verticalLayout_8.addWidget(self.label_19)

        self.newDatasetForm_2 = QWidget(self.newDatasetPage)
        self.newDatasetForm_2.setObjectName(u"newDatasetForm_2")
        self._6 = QFormLayout(self.newDatasetForm_2)
        self._6.setObjectName(u"_6")
        self.datasetNameLabel_2 = QLabel(self.newDatasetForm_2)
        self.datasetNameLabel_2.setObjectName(u"datasetNameLabel_2")

        self._6.setWidget(0, QFormLayout.LabelRole, self.datasetNameLabel_2)

        self.datasetNameLineEdit = QLineEdit(self.newDatasetForm_2)
        self.datasetNameLineEdit.setObjectName(u"datasetNameLineEdit")

        self._6.setWidget(0, QFormLayout.FieldRole, self.datasetNameLineEdit)

        self.datasetIDLabel_2 = QLabel(self.newDatasetForm_2)
        self.datasetIDLabel_2.setObjectName(u"datasetIDLabel_2")

        self._6.setWidget(1, QFormLayout.LabelRole, self.datasetIDLabel_2)

        self.datasetIDLineEdit = QLineEdit(self.newDatasetForm_2)
        self.datasetIDLineEdit.setObjectName(u"datasetIDLineEdit")

        self._6.setWidget(1, QFormLayout.FieldRole, self.datasetIDLineEdit)

        self.label_26 = QLabel(self.newDatasetForm_2)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setOpenExternalLinks(True)

        self._6.setWidget(2, QFormLayout.FieldRole, self.label_26)

        self.datasetInstrumentLineEdit = QLineEdit(self.newDatasetForm_2)
        self.datasetInstrumentLineEdit.setObjectName(u"datasetInstrumentLineEdit")

        self._6.setWidget(3, QFormLayout.FieldRole, self.datasetInstrumentLineEdit)

        self.datasetInstrumentLabel = QLabel(self.newDatasetForm_2)
        self.datasetInstrumentLabel.setObjectName(u"datasetInstrumentLabel")

        self._6.setWidget(3, QFormLayout.LabelRole, self.datasetInstrumentLabel)

        self.label_39 = QLabel(self.newDatasetForm_2)
        self.label_39.setObjectName(u"label_39")

        self._6.setWidget(4, QFormLayout.FieldRole, self.label_39)


        self.verticalLayout_8.addWidget(self.newDatasetForm_2)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_6)

        self.label_6 = QLabel(self.newDatasetPage)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_8.addWidget(self.label_6)

        ImportDataFiles.setPage(12, self.newDatasetPage)
        self.skipProjectPage = SkipProjectIntroPage()
        self.skipProjectPage.setObjectName(u"skipProjectPage")
        self.verticalLayout_7 = QVBoxLayout(self.skipProjectPage)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_28 = QLabel(self.skipProjectPage)
        self.label_28.setObjectName(u"label_28")
        font1 = QFont()
        font1.setFamilies([u"Noto Sans"])
        font1.setPointSize(17)
        font1.setBold(True)
        font1.setItalic(False)
        self.label_28.setFont(font1)

        self.verticalLayout_7.addWidget(self.label_28)

        self.label_27 = QLabel(self.skipProjectPage)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_7.addWidget(self.label_27)

        self.existingProjectForm_3 = QWidget(self.skipProjectPage)
        self.existingProjectForm_3.setObjectName(u"existingProjectForm_3")
        self.gridLayout_2 = QGridLayout(self.existingProjectForm_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_29 = QLabel(self.existingProjectForm_3)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_2.addWidget(self.label_29, 0, 0, 2, 2)

        self.skipProject_existingProjectName = QLabel(self.existingProjectForm_3)
        self.skipProject_existingProjectName.setObjectName(u"skipProject_existingProjectName")

        self.gridLayout_2.addWidget(self.skipProject_existingProjectName, 1, 1, 1, 1)


        self.verticalLayout_7.addWidget(self.existingProjectForm_3)

        self.verticalSpacer_7 = QSpacerItem(20, 305, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_7)

        ImportDataFiles.addPage(self.skipProjectPage)
        self.skipExpPage = SkipExperimentIntroPage()
        self.skipExpPage.setObjectName(u"skipExpPage")
        self.verticalLayout_9 = QVBoxLayout(self.skipExpPage)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_30 = QLabel(self.skipExpPage)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font1)

        self.verticalLayout_9.addWidget(self.label_30)

        self.label_33 = QLabel(self.skipExpPage)
        self.label_33.setObjectName(u"label_33")

        self.verticalLayout_9.addWidget(self.label_33)

        self.existingProjectForm_4 = QWidget(self.skipExpPage)
        self.existingProjectForm_4.setObjectName(u"existingProjectForm_4")
        self.gridLayout_8 = QGridLayout(self.existingProjectForm_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_31 = QLabel(self.existingProjectForm_4)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_8.addWidget(self.label_31, 0, 0, 1, 1)

        self.label_32 = QLabel(self.existingProjectForm_4)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_8.addWidget(self.label_32, 1, 0, 1, 1)

        self.skipExp_existingProjectName = QLabel(self.existingProjectForm_4)
        self.skipExp_existingProjectName.setObjectName(u"skipExp_existingProjectName")

        self.gridLayout_8.addWidget(self.skipExp_existingProjectName, 0, 1, 1, 1)

        self.skipExp_existingExpName = QLabel(self.existingProjectForm_4)
        self.skipExp_existingExpName.setObjectName(u"skipExp_existingExpName")

        self.gridLayout_8.addWidget(self.skipExp_existingExpName, 1, 1, 1, 1)


        self.verticalLayout_9.addWidget(self.existingProjectForm_4)

        self.verticalSpacer_8 = QSpacerItem(20, 281, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_8)

        ImportDataFiles.addPage(self.skipExpPage)
        self.skipDatasetPage = SkipDatasetIntroPage()
        self.skipDatasetPage.setObjectName(u"skipDatasetPage")
        self.verticalLayout_10 = QVBoxLayout(self.skipDatasetPage)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_35 = QLabel(self.skipDatasetPage)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setFont(font1)

        self.verticalLayout_10.addWidget(self.label_35)

        self.label_34 = QLabel(self.skipDatasetPage)
        self.label_34.setObjectName(u"label_34")

        self.verticalLayout_10.addWidget(self.label_34)

        self.existingDatasetForm_2 = QWidget(self.skipDatasetPage)
        self.existingDatasetForm_2.setObjectName(u"existingDatasetForm_2")
        self.gridLayout_13 = QGridLayout(self.existingDatasetForm_2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_36 = QLabel(self.existingDatasetForm_2)
        self.label_36.setObjectName(u"label_36")

        self.gridLayout_13.addWidget(self.label_36, 0, 0, 1, 1)

        self.label_37 = QLabel(self.existingDatasetForm_2)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_13.addWidget(self.label_37, 1, 0, 1, 1)

        self.label_38 = QLabel(self.existingDatasetForm_2)
        self.label_38.setObjectName(u"label_38")

        self.gridLayout_13.addWidget(self.label_38, 2, 0, 1, 1)

        self.skipDataset_existingExpName = QLabel(self.existingDatasetForm_2)
        self.skipDataset_existingExpName.setObjectName(u"skipDataset_existingExpName")

        self.gridLayout_13.addWidget(self.skipDataset_existingExpName, 0, 1, 1, 1)

        self.skipDataset_existingProjectName = QLabel(self.existingDatasetForm_2)
        self.skipDataset_existingProjectName.setObjectName(u"skipDataset_existingProjectName")

        self.gridLayout_13.addWidget(self.skipDataset_existingProjectName, 1, 1, 1, 1)

        self.skipDataset_existingDatasetName = QLabel(self.existingDatasetForm_2)
        self.skipDataset_existingDatasetName.setObjectName(u"skipDataset_existingDatasetName")

        self.gridLayout_13.addWidget(self.skipDataset_existingDatasetName, 2, 1, 1, 1)


        self.verticalLayout_10.addWidget(self.existingDatasetForm_2)

        self.verticalSpacer_9 = QSpacerItem(20, 253, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_9)

        ImportDataFiles.addPage(self.skipDatasetPage)
        self.includedFilesPage = IncludedFilesPage()
        self.includedFilesPage.setObjectName(u"includedFilesPage")
        self.gridLayout = QGridLayout(self.includedFilesPage)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_23 = QLabel(self.includedFilesPage)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font)

        self.verticalLayout_5.addWidget(self.label_23)

        self.label_7 = QLabel(self.includedFilesPage)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_5.addWidget(self.label_7)

        self.datafiletableWidget = QTableWidget(self.includedFilesPage)
        if (self.datafiletableWidget.columnCount() < 3):
            self.datafiletableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.datafiletableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.datafiletableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.datafiletableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.datafiletableWidget.setObjectName(u"datafiletableWidget")
        self.datafiletableWidget.setMinimumSize(QSize(540, 0))
        self.datafiletableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.datafiletableWidget.setAutoScroll(True)
        self.datafiletableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.datafiletableWidget.horizontalHeader().setVisible(False)
        self.datafiletableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.datafiletableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.datafiletableWidget.horizontalHeader().setHighlightSections(True)
        self.datafiletableWidget.horizontalHeader().setProperty("showSortIndicator", True)
        self.datafiletableWidget.horizontalHeader().setStretchLastSection(True)
        self.datafiletableWidget.verticalHeader().setVisible(False)
        self.datafiletableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.datafiletableWidget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_5.addWidget(self.datafiletableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dirAddPushButton = QPushButton(self.includedFilesPage)
        self.dirAddPushButton.setObjectName(u"dirAddPushButton")

        self.horizontalLayout.addWidget(self.dirAddPushButton)

        self.datafileAddPushButton = QPushButton(self.includedFilesPage)
        self.datafileAddPushButton.setObjectName(u"datafileAddPushButton")

        self.horizontalLayout.addWidget(self.datafileAddPushButton)

        self.datafileDeletePushButton = QPushButton(self.includedFilesPage)
        self.datafileDeletePushButton.setObjectName(u"datafileDeletePushButton")

        self.horizontalLayout.addWidget(self.datafileDeletePushButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.label_8 = QLabel(self.includedFilesPage)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_5.addWidget(self.label_8)


        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)

        ImportDataFiles.setPage(669, self.includedFilesPage)
        QWidget.setTabOrder(self.existingProjectRadioButton, self.existingProjectList)
        QWidget.setTabOrder(self.existingProjectList, self.newProjectRadioButton)
        QWidget.setTabOrder(self.newProjectRadioButton, self.projectNameLineEdit)
        QWidget.setTabOrder(self.projectNameLineEdit, self.projectIDLineEdit)
        QWidget.setTabOrder(self.projectIDLineEdit, self.piLineEdit)
        QWidget.setTabOrder(self.piLineEdit, self.projectDescriptionTextEdit)
        QWidget.setTabOrder(self.projectDescriptionTextEdit, self.existingExperimentList)
        QWidget.setTabOrder(self.existingExperimentList, self.newExperimentRadioButton)
        QWidget.setTabOrder(self.newExperimentRadioButton, self.experimentNameLineEdit)
        QWidget.setTabOrder(self.experimentNameLineEdit, self.experimentIDLineEdit)
        QWidget.setTabOrder(self.experimentIDLineEdit, self.experimentDescriptionLineEdit)
        QWidget.setTabOrder(self.experimentDescriptionLineEdit, self.existingDatasetRadioButton)
        QWidget.setTabOrder(self.existingDatasetRadioButton, self.existingDatasetList)
        QWidget.setTabOrder(self.existingDatasetList, self.newDatasetRadioButton)
        QWidget.setTabOrder(self.newDatasetRadioButton, self.datasetNameLineEdit)
        QWidget.setTabOrder(self.datasetNameLineEdit, self.datasetIDLineEdit)
        QWidget.setTabOrder(self.datasetIDLineEdit, self.datafiletableWidget)
        QWidget.setTabOrder(self.datafiletableWidget, self.dirAddPushButton)
        QWidget.setTabOrder(self.dirAddPushButton, self.datafileAddPushButton)
        QWidget.setTabOrder(self.datafileAddPushButton, self.datafileDeletePushButton)
        QWidget.setTabOrder(self.datafileDeletePushButton, self.existingExperimentRadioButton)

        self.retranslateUi(ImportDataFiles)

        QMetaObject.connectSlotsByName(ImportDataFiles)
    # setupUi

    def retranslateUi(self, ImportDataFiles):
        ImportDataFiles.setWindowTitle(QCoreApplication.translate("ImportDataFiles", u"Import Data", None))
        self.label_14.setText(QCoreApplication.translate("ImportDataFiles", u"Welcome", None))
        self.label_9.setText(QCoreApplication.translate("ImportDataFiles", u"This dialog will get you started with importing your data and organising them.", None))
        self.label_12.setText("")
        self.label_10.setText(QCoreApplication.translate("ImportDataFiles", u"In MyTardis, data are organised in a hierarchy. Files are grouped into Datasets. Datasets are organised into Experiments. Experiments belong to a Project. You can attach metadata at each level to make it easier for you and your collaborators to find and reuse your data. ", None))
        self.label_11.setText(QCoreApplication.translate("ImportDataFiles", u"This dialog will help you create the Project, Experiment and Dataset to put your files under. You can re-run this dialog for other files that need to be organised separately.", None))
        self.label_4.setText(QCoreApplication.translate("ImportDataFiles", u"Project", None))
        self.label.setText(QCoreApplication.translate("ImportDataFiles", u"First, let's find or create the project you are adding the data files to.", None))
        self.existingProjectRadioButton.setText(QCoreApplication.translate("ImportDataFiles", u"Add this data into an existing project.", None))
        self.newProjectRadioButton.setText(QCoreApplication.translate("ImportDataFiles", u"Create a new project for this data.", None))
        self.label_13.setText(QCoreApplication.translate("ImportDataFiles", u"Enter some basic details for the new project, then click next.", None))
        self.projectNameLabel.setText(QCoreApplication.translate("ImportDataFiles", u"Project name", None))
        self.projectNameLineEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"A human-readable name for your project", None))
        self.projectIDLabel.setText(QCoreApplication.translate("ImportDataFiles", u"Project identifier", None))
        self.projectIDLineEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"A label for the Project, must be unique across Projects. Use letters and numbers.", None))
        self.label_24.setText(QCoreApplication.translate("ImportDataFiles", u"<a href=\"https://uoa-eresearch.github.io/mytardis_ime/user/identifiers.html\">What should I use as an identifier?</a>", None))
        self.projectDescriptionLabel.setText(QCoreApplication.translate("ImportDataFiles", u"Description", None))
        self.piLabel.setText(QCoreApplication.translate("ImportDataFiles", u"Principal Investigator", None))
        self.piLineEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"Username of the researcher primarily responsible for this project.", None))
        self.projectDescriptionTextEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"Description of your project to differentiate it from others", None))
        self.label_15.setText(QCoreApplication.translate("ImportDataFiles", u"You can add more metadata and access controls for the project later.", None))
        self.label_2.setText(QCoreApplication.translate("ImportDataFiles", u"New Project", None))
        self.label_18.setText(QCoreApplication.translate("ImportDataFiles", u"Experiment", None))
        self.label_3.setText(QCoreApplication.translate("ImportDataFiles", u"Now, let's find or create the experiment the data files fits under.", None))
        self.existingExperimentRadioButton.setText(QCoreApplication.translate("ImportDataFiles", u"Add this data to an existing experiment.", None))
        self.newExperimentRadioButton.setText(QCoreApplication.translate("ImportDataFiles", u"Create a new experiment for this data.", None))
        self.label_20.setText(QCoreApplication.translate("ImportDataFiles", u"New Experiment", None))
        self.label_16.setText(QCoreApplication.translate("ImportDataFiles", u"Enter some basic details for the new experiment, then click next.", None))
        self.experimentNameLabel.setText(QCoreApplication.translate("ImportDataFiles", u"Experiment name", None))
        self.experimentNameLineEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"A human-readable name for your experiment", None))
        self.experimentIDLabel.setText(QCoreApplication.translate("ImportDataFiles", u"Experiment identifier", None))
        self.experimentIDLineEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"A label for the Experiment, must be unique across Experiments. Use letters and numbers.", None))
        self.label_25.setText(QCoreApplication.translate("ImportDataFiles", u"<a href=\"https://uoa-eresearch.github.io/mytardis_ime/user/identifiers.html\">What should I use as an identifier?</a>", None))
        self.experimentdescriptionLabel.setText(QCoreApplication.translate("ImportDataFiles", u"Description", None))
        self.experimentDescriptionLineEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"Optional description of the experiment", None))
        self.label_17.setText(QCoreApplication.translate("ImportDataFiles", u"You can add more metadata and access controls for the experiment later.", None))
        self.label_21.setText(QCoreApplication.translate("ImportDataFiles", u"Dataset", None))
        self.label_5.setText(QCoreApplication.translate("ImportDataFiles", u"Nearly there! Let's find or create the dataset for your data files.", None))
        self.existingDatasetRadioButton.setText(QCoreApplication.translate("ImportDataFiles", u"Add this data to an existing dataset.", None))
        self.newDatasetRadioButton.setText(QCoreApplication.translate("ImportDataFiles", u"Create a new dataset for this data.", None))
        self.label_22.setText(QCoreApplication.translate("ImportDataFiles", u"New Dataset", None))
        self.label_19.setText(QCoreApplication.translate("ImportDataFiles", u"Enter some basic details for the new dataset, then click next.", None))
        self.datasetNameLabel_2.setText(QCoreApplication.translate("ImportDataFiles", u"Dataset name", None))
        self.datasetNameLineEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"A human-readable name for your dataset", None))
        self.datasetIDLabel_2.setText(QCoreApplication.translate("ImportDataFiles", u"Dataset identifier", None))
        self.datasetIDLineEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"A label for the Dataset, must be unique across Datasets. Use letters and numbers.", None))
        self.label_26.setText(QCoreApplication.translate("ImportDataFiles", u"<a href=\"https://uoa-eresearch.github.io/mytardis_ime/user/identifiers.html\">What should I use as an identifier?</a>", None))
        self.datasetInstrumentLineEdit.setPlaceholderText(QCoreApplication.translate("ImportDataFiles", u"A unique identifier to the instrument that the data was generated on. Currently there is no standard persistent identifier that has widespread community adoption (DOIs are the most likely candidate).", None))
        self.datasetInstrumentLabel.setText(QCoreApplication.translate("ImportDataFiles", u"Instrument identifier", None))
        self.label_39.setText(QCoreApplication.translate("ImportDataFiles", u"<a href=\"https://uoa-eresearch.github.io/mytardis_ime/user/finding-instrument-id.html\">How to find my instrument's persistent identifier(PID)?", None))
        self.label_6.setText(QCoreApplication.translate("ImportDataFiles", u"You can add more metadata and access controls for the dataset later.", None))
        self.label_28.setText(QCoreApplication.translate("ImportDataFiles", u"Add an Experiment to a Project", None))
        self.label_27.setText(QCoreApplication.translate("ImportDataFiles", u"You will be adding a new Experiment into the following Project:", None))
        self.label_29.setText(QCoreApplication.translate("ImportDataFiles", u"Project", None))
        self.skipProject_existingProjectName.setText("")
        self.label_30.setText(QCoreApplication.translate("ImportDataFiles", u"Add a Dataset to an Experiment", None))
        self.label_33.setText(QCoreApplication.translate("ImportDataFiles", u"You will be adding a new Dataset into the following Project and Experiment:", None))
        self.label_31.setText(QCoreApplication.translate("ImportDataFiles", u"Project", None))
        self.label_32.setText(QCoreApplication.translate("ImportDataFiles", u"Experiment", None))
        self.skipExp_existingProjectName.setText("")
        self.skipExp_existingExpName.setText("")
        self.label_35.setText(QCoreApplication.translate("ImportDataFiles", u"Add Datafiles to a Dataset", None))
        self.label_34.setText(QCoreApplication.translate("ImportDataFiles", u"You will be adding new data files into the following Project, Experiment, and Dataset:", None))
        self.label_36.setText(QCoreApplication.translate("ImportDataFiles", u"Project", None))
        self.label_37.setText(QCoreApplication.translate("ImportDataFiles", u"Experiment", None))
        self.label_38.setText(QCoreApplication.translate("ImportDataFiles", u"Dataset", None))
        self.skipDataset_existingExpName.setText("")
        self.skipDataset_existingProjectName.setText("")
        self.skipDataset_existingDatasetName.setText("")
        self.label_23.setText(QCoreApplication.translate("ImportDataFiles", u"Datafiles", None))
        self.label_7.setText(QCoreApplication.translate("ImportDataFiles", u"Finally, choose the files you wish to include in this dataset.", None))
        ___qtablewidgetitem = self.datafiletableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("ImportDataFiles", u"Name", None));
        ___qtablewidgetitem1 = self.datafiletableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("ImportDataFiles", u"Size", None));
        ___qtablewidgetitem2 = self.datafiletableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("ImportDataFiles", u"File Path", None));
#if QT_CONFIG(tooltip)
        self.datafiletableWidget.setToolTip(QCoreApplication.translate("ImportDataFiles", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.dirAddPushButton.setText(QCoreApplication.translate("ImportDataFiles", u"Add a folder...", None))
        self.datafileAddPushButton.setText(QCoreApplication.translate("ImportDataFiles", u"Add files", None))
        self.datafileDeletePushButton.setText(QCoreApplication.translate("ImportDataFiles", u"Remove files", None))
        self.label_8.setText(QCoreApplication.translate("ImportDataFiles", u"You can override inherited metadata and access controls later.", None))
    # retranslateUi

