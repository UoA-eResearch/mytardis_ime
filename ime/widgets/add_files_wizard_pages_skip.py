"""
add_files_wizard_pages.py - custom logic for add files wizard pages.
"""
import typing
from PyQt5.QtWidgets import QWidget, QWizardPage

from ime.ui.ui_add_files_wizard_skip import Ui_ImportDataFiles
import ime.widgets.add_files_wizard as afw
from ime.qt_models import IngestionMetadataModel

class ProjectPage(QWizardPage):

    def selected_existing_project_changed(self, idx: int):
        # Look up and record the selected existing project.
        project = self.model.instance(idx)
        self.wizard().selected_existing_project = project

    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        wizard = self.wizard()
        # Display the list of projects.
        list_view = wizard.ui.existingProjectList
        self.model = wizard.metadataModel.projects.proxy(['project_name'])
        self.model.set_read_only(True)
        list_view.setModel(self.model)
        self.selected_existing_project_changed(wizard.ui.existingProjectList.currentIndex())
        list_view.currentIndexChanged.connect(self.selected_existing_project_changed)

    def cleanupPage(self) -> None:
        self.wizard().ui.existingProjectList.currentIndexChanged.disconnect()

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        return wizard.page_ids['newExperimentPage']
    
    def isComplete(self) -> bool:
        # Block Next button until required fields are filled.
        return (self.field('isExistingProject') and self.field('existingProject') is not None)

class PExperimentPage(QWizardPage):
    def selected_existing_pe_changed(self, idx_p: int, idx_e: int):
        # Look up and record the selected existing project and experiment.
        project = self.model.instance(idx_p)
        experiment = self.model.instance(idx_e)
        self.wizard().selected_existing_project = project
        self.wizard().selected_existing_experiment = experiment

    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        wizard = self.wizard()
        # Display the list of projects
        list_view_pro = wizard.ui.existingProjectList_2

        # Only show experiments from the selected project.
        list_view_exp = wizard.ui.existingExperimentList_1
        self.model = wizard.metadataModel.projects.proxy(['project_name'])
        self.model.set_read_only(True)
        list_view_pro.setModel(self.model)
        list_view_exp.setModel(self.model)

        #project = wizard.selected_existing_project
        #self.model = wizard.metadataModel.experiments_for_project(project)
        #self.model.set_read_only(True)
    
        self.model.set_show_fields(['project_name','experiment_name'])

        #wizard.ui.existingProjectList_2.setModel(self.model)
        #self.selected_existing_pe_changed(wizard.ui.existingProjectList_2.currentIndex(), wizard.ui.existingExperimentList_1.currentIndex())
        #wizard.ui.existingExperimentList_1.currentIndexChanged.connect(self.selected_existing_pe_changed)
        #list_view.currentIndexChanged.connect(self.selected_existing_pe_changed)

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        return wizard.page_ids['newDatasetPage']

    def cleanupPage(self) -> None:
        self.wizard().ui.existingExperimentList_1.currentIndexChanged.disconnect()
        self.wizard().ui.existingProjectList_2.currentIndexChanged.disconnect()

    def isComplete(self) -> bool:
        return self.field('existingProject') is not None and self.field('existingExperiment') is not None

class PEDatasetPage(QWizardPage):
    def selected_existing_dataset_changed(self, idx: int):
        # Look up and record the selected existing dataset.
        ds = self.model.instance(idx)
        ## show existing projets, experiments 
        project = self.model.instance(idx)
        self.wizard().selected_existing_project = project
        exp = self.model.instance(self.wizard.ui.existingExperimentList.currentIndex())
        self.wizard().selected_existing_experiment = exp
        self.wizard().selected_existing_dataset = ds

    def wizard(self):
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        wizard = self.wizard()
        exp = wizard.selected_existing_experiment
        # Only show datasets under the selected experiment.
        self.model = wizard.metadataModel.datasets_for_experiment(exp)
        self.model.set_read_only(True)
        self.model.set_show_fields(['dataset_name'])
        wizard.ui.existingDatasetList.setModel(self.model)
        self.selected_existing_dataset_changed(wizard.ui.existingDatasetList.currentIndex())
        wizard.ui.existingDatasetList.currentIndexChanged.connect(self.selected_existing_dataset_changed)

    def cleanupPage(self) -> None:
        self.wizard().ui.existingDatasetList.currentIndexChanged.disconnect()

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        return wizard.page_ids['includedFilesPage']

    def isComplete(self) -> bool:
        return (self.field('isExistingProject') and self.field('existingProject') is not None) and (self.field('isExistingExperiment') and self.field('existingExperiment') is not None) and (self.field('isExistingDataset') and self.field("existingDataset") is not None)