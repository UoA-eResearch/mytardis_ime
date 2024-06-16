import typing

from PySide6.QtWidgets import QWizardPage

import ime.widgets.add_files_wizard.wizard as afw


class SkipExperimentIntroPage(QWizardPage):
    """A wizard page for selecting an existing project and experiment or creating a new one."""

    def wizard(self) -> "afw.AddFilesWizard":
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

        # Checks eproject and experiment are set.
        assert exp is not None
        assert project is not None

        # Sets the text on project and experiment.
        wizard.ui.skipExp_existingExpName.setText(exp.title)
        wizard.ui.skipExp_existingProjectName.setText(project.name)

    def nextId(self) -> int:
        """Override method for determining which page to advance to next.

        Returns:
            int: The page ID for next page to advance to.
        """
        return self.wizard().page_ids["datasetPage"]
