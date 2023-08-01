"""
add_files_wizard_pages.py - custom logic for add files wizard pages.
"""
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QWizardPage
import ime.widgets.add_files_wizard as afw

class SkipProjectIntroPage(QWizardPage):
    """ A wizard page for selecting an existing project or creating a new one.

    Args:
        QWizardPage (_type_):  The type of the parent class.
    """
    def wizard(self) -> afw.AddFilesWizard:
        # Add type cast so type checker isn't annoyed below.
        """Return the wizard object with type cast.

        Returns:
            _type_: _description_
        """
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        """Display the list of projects and initialize the selected project."""
        wizard = self.wizard()
        # Display the list of projects.
        project = wizard.selected_existing_project
        assert project is not None
        wizard.ui.skipProject_existingProjectName.setText(project.name)

    def nextId(self) -> int:
        return self.wizard().page_ids["experimentPage"]

class SkipExperimentIntroPage(QWizardPage):
    """A wizard page for selecting an existing project and experiment or creating a new one."""
    
    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        """
        Return the wizard object with type casting.

        Returns:
            The wizard object with type casting.
        """
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        """
        Initialize the wizard page with a list of projects and experiments.
        """
        wizard = self.wizard()

        exp = wizard.selected_existing_experiment
        project = wizard.selected_existing_project

        assert exp is not None
        assert project is not None

        wizard.ui.skipExp_existingExpName.setText(exp.title)
        wizard.ui.skipExp_existingProjectName.setText(project.name)

    def nextId(self) -> int:
        return self.wizard().page_ids["datasetPage"]

class SkipDatasetIntroPage(QWizardPage):
    """A wizard page for selecting an existing project, experiment, and dataset.

    Args:
        QWizardPage (_type_): The type of the parent class.
    """
    def wizard(self):
        """Returns the wizard object.

        Returns:
            afw.AddFilesWizardSkipDataset: The wizard object.
        """
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        """Initializes the wizard page."""

        wizard = self.wizard()
        ds = wizard.selected_existing_dataset
        exp = wizard.selected_existing_experiment
        project = wizard.selected_existing_project

        assert project is not None
        assert exp is not None
        assert ds is not None

        wizard.ui.skipDataset_existingDatasetName.setText(ds.dataset_name)
        wizard.ui.skipDataset_existingExpName.setText(exp.title)
        wizard.ui.skipDataset_existingProjectName.setText(project.name)

    def nextId(self) -> int:
        return self.wizard().page_ids["includedFilesPage"]