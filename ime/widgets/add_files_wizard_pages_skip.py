"""
add_files_wizard_pages.py - custom logic for add files wizard pages.
"""
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QWizardPage
import ime.widgets.add_files_wizard as afw

class ProjectPage(QWizardPage):
    """ A wizard page for selecting an existing project or creating a new one.

    Args:
        QWizardPage (_type_):  The type of the parent class.
    """
    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        """Return the wizard object with type cast.

        Returns:
            _type_: _description_
        """
        return typing.cast(afw.AddFilesWizardSkipProject, super().wizard())

    def initializePage(self) -> None:
        """Display the list of projects and initialize the selected project."""
        wizard = self.wizard()
        # Display the list of projects.
        pro = wizard.pro_passed

        wizard.ui.existingProjectList_1.addItem(pro.name)

        wizard.selected_existing_project = pro

    def cleanupPage(self) -> None:
        """Disconnect the currentIndexChanged signal."""
        self.wizard().ui.existingProjectList_1.currentIndexChanged.disconnect()
    
    def isComplete(self) -> bool:
        """Return True if the required fields are filled.

        Returns:
            bool: True if the required fields are filled.
        """
        return self.field('isExistingProject') is not None

class PExperimentPage(QWizardPage):
    """A wizard page for selecting an existing project and experiment or creating a new one."""
    
    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        """
        Return the wizard object with type casting.

        Returns:
            The wizard object with type casting.
        """
        return typing.cast(afw.AddFilesWizardSkipExperiment, super().wizard())

    def initializePage(self) -> None:
        """
        Initialize the wizard page with a list of projects and experiments.
        """
        wizard = self.wizard()

        exp = wizard.exp_passed
        pro = wizard.pro_passed

        wizard.ui.existingExperimentList_1.addItem(exp.title)
        wizard.ui.existingProjectList_2.addItem(pro.name)

        wizard.selected_existing_project = pro
        wizard.selected_existing_experiment = exp

    def cleanupPage(self) -> None:
        """
        Disconnect signals when the wizard page is closed.
        """
        self.wizard().ui.existingExperimentList_1.currentIndexChanged.disconnect()
        self.wizard().ui.existingProjectList_2.currentIndexChanged.disconnect()

    def isComplete(self) -> bool:
        """
        Check if the user has selected an existing project and experiment.

        Returns:
            True if the user has selected an existing project and experiment, False otherwise.
        """
        return self.field('isExistingProject') is not None and self.field('isExistingExperiment') is not None

class PEDatasetPage(QWizardPage):
    """A wizard page for selecting an existing project, experiment, and dataset.

    Args:
        QWizardPage (_type_): The type of the parent class.
    """
    def wizard(self):
        """Returns the wizard object.

        Returns:
            afw.AddFilesWizardSkipDataset: The wizard object.
        """
        return typing.cast(afw.AddFilesWizardSkipDataset, super().wizard())

    def initializePage(self) -> None:
        """Initializes the wizard page."""

        wizard = self.wizard()
        ds = wizard.ds_passed
        exp = wizard.exp_passed
        pro = wizard.pro_passed

        wizard.ui.existingDatasetList_1.addItem(ds.dataset_name)
        wizard.ui.existingExperimentList_2.addItem(exp.title)
        wizard.ui.existingProjectList_3.addItem(pro.name)

        wizard.selected_existing_project = pro
        wizard.selected_existing_experiment = exp
        wizard.selected_existing_dataset = ds

    def cleanupPage(self) -> None:
        """Cleans up the wizard page."""
        self.wizard().ui.existingDatasetList_1.currentIndexChanged.disconnect()
        self.wizard().ui.existingExperimentList_2.currentIndexChanged.disconnect()
        self.wizard().ui.existingProjectList_3.currentIndexChanged.disconnect()

    def isComplete(self) -> bool:
        """Checks whether the selection of existing project, experiment, and dataset is complete.

        Returns:
            bool: True if the selection is complete; False otherwise.
        """
        return self.field('isExistingProject') is not None and self.field('isExistingExperiment') is not None and self.field('isExistingDataset') is not None