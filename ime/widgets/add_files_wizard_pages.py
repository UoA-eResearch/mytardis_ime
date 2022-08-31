"""
add_files_wizard_pages.py - custom logic for add files wizard pages.
"""
import typing
from PyQt5.QtWidgets import QWidget, QWizardPage

from ime.ui.ui_add_files_wizard import Ui_ImportDataFiles


class ProjectPage(QWizardPage):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

    def initializePage(self) -> None:
        self.setField('isExistingProject', True)
        wizard : Ui_ImportDataFiles = self.wizard().ui
        wizard.existingProjectForm.setVisible(True)
        wizard.newProjectForm.setVisible(False)

    def isComplete(self) -> bool:
        return ((self.field('isNewProject') and 
                self.field('projectNameLineEdit').strip() != "" and
                self.field('projectIDLineEdit').strip() != "") or
                (self.field('isExistingProject') and
                self.field('existingProject') != -1))

class ExperimentPage(QWizardPage):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

    def initializePage(self) -> None:
        wizard : Ui_ImportDataFiles = self.wizard().ui
        # First decide we need to show both new and existing.
        should_disable_existing = self.field('isNewProject')
        wizard.existingExperimentRadioButton.setDisabled(should_disable_existing)
        if should_disable_existing:
            self.setField('isNewExperiment', True)
            self.setField('isExistingExperiment', False)
            wizard.existingExperimentForm.setVisible(False)
            wizard.newExperimentForm.setVisible(True)
        else:
            self.setField('isNewExperiment', False)
            self.setField('isExistingExperiment', True)
            wizard.existingExperimentForm.setVisible(True)
            wizard.newExperimentForm.setVisible(False)

    def isComplete(self) -> bool:
        return ((self.field('isNewExperiment') and 
                self.field('experimentNameLineEdit').strip() != "" and
                self.field('experimentIDLineEdit').strip() != "") or
                (self.field('isExistingExperiment') and
                self.field('existingExperiment') != -1))

class DatasetPage(QWizardPage):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

    def initializePage(self) -> None:
        wizard : Ui_ImportDataFiles = self.wizard().ui
        self.setField('isExistingDataset', False)
        should_disable_existing = self.field('isNewExperiment')
        wizard.existingDatasetRadioButton.setDisabled(should_disable_existing)
        if should_disable_existing:
            self.setField('isNewDataset', True)
            self.setField('isExistingDataset', False)
            wizard.existingDatasetForm.setVisible(False)
            wizard.newDatasetForm.setVisible(True)
        else:
            self.setField('isNewDataset', False)
            self.setField('isExistingDataset', True)
            wizard.existingDatasetForm.setVisible(True)
            wizard.newDatasetForm.setVisible(False)

    def isComplete(self) -> bool:
        return ((self.field('isNewDataset') and 
                self.field('datasetNameLineEdit').strip() != "" and
                self.field('datasetIDLineEdit').strip() != "") or
                (self.field('isExistingDataset') and
                self.field('existingDataset') != -1))