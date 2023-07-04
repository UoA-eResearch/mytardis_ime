"""
add_files_wizard_pages.py - custom logic for add files wizard pages.
"""
import typing
from PyQt5.QtWidgets import QWidget, QWizardPage

from ime.ui.ui_add_files_wizard import Ui_ImportDataFiles
import ime.widgets.add_files_wizard as afw
from ime.qt_models import IngestionMetadataModel

class ProjectPage(QWizardPage):

    def selected_existing_project_changed(self, idx: int) -> None:
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
        self.model = wizard.metadataModel.projects.proxy(['name'])
        self.model.set_read_only(True)
        list_view.setModel(self.model)
        self.selected_existing_project_changed(wizard.ui.existingProjectList.currentIndex())
        list_view.currentIndexChanged.connect(self.selected_existing_project_changed)

    def cleanupPage(self) -> None:
        self.wizard().ui.existingProjectList.currentIndexChanged.disconnect()

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field('isNewProject'):
            # Go to the new project page
            return wizard.page_ids['newProjectPage']
        else:
            return wizard.page_ids['experimentPage']

    def isComplete(self) -> bool:
        # Block Next button until required fields are filled.
        return self.field('isNewProject') or (self.field('isExistingProject') and self.field('existingProject') is not None)

class ExperimentPage(QWizardPage):
    def selected_existing_exp_changed(self,idx: int) -> None:
        # Look up and record the selected existing experiment.
        wizard = self.wizard()
        exp = self.model.instance(wizard.ui.existingExperimentList.currentIndex())
        wizard.selected_existing_experiment = exp


    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        wizard = self.wizard()
        # Only show experiments from the selected project.
        project = wizard.selected_existing_project
        self.model = wizard.metadataModel.experiments_for_project(project)
        self.model.set_read_only(True)
        self.model.set_show_fields(['title'])
        wizard.ui.existingExperimentList.setModel(self.model)
        self.selected_existing_exp_changed(wizard.ui.existingExperimentList.currentIndex())
        wizard.ui.existingExperimentList.currentIndexChanged.connect(self.selected_existing_exp_changed)

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field('isNewExperiment'):
            # Go to the new project page
            return wizard.page_ids['newExperimentPage']
        else:
            return wizard.page_ids['datasetPage']

    def cleanupPage(self) -> None:
        self.wizard().ui.existingExperimentList.currentIndexChanged.disconnect()

    def isComplete(self) -> bool:
        return self.field('isNewExperiment') or (self.field('isExistingExperiment') and self.field('existingExperiment') is not None)

class DatasetPage(QWizardPage):
    def selected_existing_dataset_changed(self, idx: int) -> None:
        # Look up and record the selected existing dataset.
        ds = self.model.instance(idx)
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
        if self.field('isNewDataset'):
            # Go to the new project page
            return wizard.page_ids['newDatasetPage']
        else:
            return wizard.page_ids['includedFilesPage']

    def isComplete(self) -> bool:
        return self.field('isNewDataset') or (self.field('isExistingDataset') and self.field("existingDataset") is not None)