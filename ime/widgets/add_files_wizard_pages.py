"""
add_files_wizard_pages.py - custom logic for add files wizard pages.
"""
import typing
from PyQt5.QtWidgets import QWidget, QWizardPage

from ime.ui.ui_add_files_wizard import Ui_ImportDataFiles
import ime.widgets.add_files_wizard as afw
from ime.qt_models import IngestionMetadataModel


class ProjectPage(QWizardPage):
    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field('isNewProject'):
            # Go to the new project page
            return wizard.page_ids['newProjectPage']
        else:
            return wizard.page_ids['existingProjectPage']

    def isComplete(self) -> bool:
        return self.field('isNewProject') or self.field('isExistingProject')

class ExperimentPage(QWizardPage):
    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field('isNewExperiment'):
            # Go to the new project page
            return wizard.page_ids['newExperimentPage']
        else:
            return wizard.page_ids['existingExperimentPage']

    def isComplete(self) -> bool:
        return self.field('isNewExperiment') or self.field('isExistingExperiment')

class DatasetPage(QWizardPage):
    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field('isNewDataset'):
            # Go to the new project page
            return wizard.page_ids['newDatasetPage']
        else:
            return wizard.page_ids['existingDatasetPage']

    def isComplete(self) -> bool:
        return self.field('isNewDataset') or self.field('isExistingDataset')

class ExistingProjectPage(QWizardPage):
    def initializePage(self) -> None:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        list_view = wizard.ui.existingProjectList
        model = wizard.metadataModel.projects.get_read_only_proxy(['project_name'])
        list_view.setModel(model)

class ExistingExperimentPage(QWizardPage):
    def initializePage(self) -> None:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        project_idx = self.field('existingProject')
        project = wizard.metadataModel.projects.instance(project_idx)
        model = wizard.metadataModel.experiments_for_project(project)
        model.set_read_only(True)
        model.set_show_fields(['experiment_name'])
        wizard.ui.existingExperimentList.setModel(model)

class ExistingDatasetPage(QWizardPage):
    def initializePage(self) -> None:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        exp_idx = self.field('existingExperiment')
        exp = wizard.metadataModel.experiments.instance(exp_idx)
        model = wizard.metadataModel.datasets_for_experiment(exp)
        model.set_read_only(True)
        model.set_show_fields(['dataset_name'])
        wizard.ui.existingDatasetList.setModel(model)
