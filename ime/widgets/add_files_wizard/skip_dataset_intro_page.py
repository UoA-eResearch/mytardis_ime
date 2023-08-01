import typing
from PyQt5.QtWidgets import QWizardPage
import ime.widgets.add_files_wizard.wizard as afw

class SkipDatasetIntroPage(QWizardPage):
    """A wizard page for selecting an existing project, experiment, and dataset.

    Args:
        QWizardPage (_type_): The type of the parent class.
    """
    def wizard(self) -> 'afw.AddFilesWizard':
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