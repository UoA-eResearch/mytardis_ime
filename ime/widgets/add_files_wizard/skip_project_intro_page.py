import typing

from PySide6.QtWidgets import QWizardPage

import ime.widgets.add_files_wizard.wizard as afw
from ime.widgets.add_files_wizard.enums import PageNames


class SkipProjectIntroPage(QWizardPage):
    """ A wizard page for selecting an existing project or creating a new one.

    Args:
        QWizardPage (_type_):  The type of the parent class.
    """
    def wizard(self) -> 'afw.AddFilesWizard':
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
        """Override method for determining the next page of the wizard.

        Returns:
            int: The page ID for the next page of the wizard.
        """
        return self.wizard().page_ids[PageNames.EXPERIMENT.value]
