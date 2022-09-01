"""
add_files_wizard_pages.py - custom logic for add files wizard pages.
"""
import typing
from PyQt5.QtWidgets import QWidget, QWizardPage

from ime.ui.ui_add_files_wizard import Ui_ImportDataFiles
import ime.widgets.add_files_wizard as afw


class ProjectPage(QWizardPage):
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

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
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

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
    def __init__(self, parent: typing.Optional[QWidget] = None) -> None:
        super().__init__(parent)

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field('isNewDataset'):
            # Go to the new project page
            return wizard.page_ids['newDatasetPage']
        else:
            return wizard.page_ids['existingDatasetPage']

    def isComplete(self) -> bool:
        return self.field('isNewDataset') or self.field('isExistingDataset')