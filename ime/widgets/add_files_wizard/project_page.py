"project_page.py - wizard page for existing project."
import typing

from PySide6.QtWidgets import QWizardPage

import ime.widgets.add_files_wizard.wizard as afw
from ime.widgets.add_files_wizard.enums import FieldNames, PageNames


class ProjectPage(QWizardPage):
    """Module for wizard project page - gives user a choice to create
    a new project or choose an existing one.
    This wizard page must be used in an afw.AddFilesWizard."""

    def selected_existing_project_changed(self, idx: int) -> None:
        """Handler method for when existing project selection has changed.

        Args:
            idx (int): The index of selected project.
        """
        # Look up and record the selected existing project.
        project = self.model.instance(idx)
        self.wizard().selected_existing_project = project

    def wizard(self) -> "afw.AddFilesWizard":
        """Override for built-in method that returns the wizard
        with more precise type-hinting.

        Returns:
            afw.AddFilesWizard: The wizard with right type hinting.
        """
        # Add type cast so type checker isn't annoyed below.
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        """Override method that initialises the page when user
        enters the page and sets up slots for signals.
        """
        wizard = self.wizard()
        # Display the list of projects.
        list_view = wizard.ui.existingProjectList
        self.model = wizard.metadataModel.projects.proxy(["name"])
        self.model.set_read_only(True)
        list_view.setModel(self.model)
        self.selected_existing_project_changed(
            wizard.ui.existingProjectList.currentIndex()
        )
        list_view.currentIndexChanged.connect(self.selected_existing_project_changed)

    def cleanupPage(self) -> None:
        """Override method that cleans up the page and signals after user
        leaves the page.
        """
        self.wizard().ui.existingProjectList.currentIndexChanged.disconnect()

    def nextId(self) -> int:
        """Override method that determines which page will be next when user
        leaves.

        Returns:
            int: The ID for the next page.
        """
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field(FieldNames.IS_NEW_PROJECT.value):
            # Go to the new project page
            return wizard.page_ids[PageNames.NEW_PROJECT.value]
        else:
            return wizard.page_ids[PageNames.EXPERIMENT.value]

    def isComplete(self) -> bool:
        """Override method that returns if the wizard advance to the next page. Checks
        the user has at least chosen to create a new project or has selected an existing
        project.

        Returns:
            bool: Whether the wizard can advance.
        """
        # Block Next button until required fields are filled.
        return self.field(FieldNames.IS_NEW_PROJECT.value) or (
            self.field(FieldNames.IS_EXISTING_PROJECT.value)
            and self.field(FieldNames.EXISTING_PROJECT.value) is not None
        )
