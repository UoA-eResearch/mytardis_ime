import typing

from PySide6.QtWidgets import QWizardPage

import ime.widgets.add_files_wizard.wizard as afw
from ime.widgets.add_files_wizard.enums import FieldNames, PageNames


class ExperimentPage(QWizardPage):
    def selected_existing_exp_changed(self, idx: int) -> None:
        # Look up and record the selected existing experiment.
        wizard = self.wizard()
        exp = self.model.instance(wizard.ui.existingExperimentList.currentIndex())
        wizard.selected_existing_experiment = exp

    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        """Lifecycle method called by Qt when entering this wizard page.
        Looks up the associated experiments for the chosen project, and displays
        the options.
        """
        wizard = self.wizard()
        # Only show experiments from the selected project.
        project = wizard.selected_existing_project
        assert project is not None
        self.model = wizard.metadataModel.experiments_for_project(project)
        self.model.set_read_only(True)
        self.model.set_show_fields(["title"])
        wizard.ui.existingExperimentList.setModel(self.model)
        wizard.ui.existingExperimentList.currentIndexChanged.connect(
            self.selected_existing_exp_changed
        )
        if self.model.rowCount() == 0:
            # When there are no experiments in selected project, disable
            # the existing dataset option.
            self.wizard().ui.existingExperimentRadioButton.setDisabled(True)
            self.wizard().ui.existingExperimentList.setDisabled(True)
            self.wizard().ui.newExperimentRadioButton.setChecked(True)
        else:
            # Set selected experiment to be the first experiment.
            self.selected_existing_exp_changed(
                wizard.ui.existingExperimentList.currentIndex()
            )

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field(FieldNames.IS_NEW_EXPERIMENT.value):
            # Go to the new project page
            return wizard.page_ids[PageNames.NEW_EXPERIMENT.value]
        else:
            return wizard.page_ids[PageNames.DATASET.value]

    def cleanupPage(self) -> None:
        """Lifecycle method called by Qt when leaving this wizard page. Cleans up
        signals and resets form controls.
        """
        self.wizard().ui.existingExperimentRadioButton.setEnabled(True)
        self.wizard().ui.existingExperimentList.setEnabled(True)
        self.wizard().ui.existingExperimentRadioButton.setChecked(True)
        self.wizard().ui.existingExperimentList.currentIndexChanged.disconnect()

    def isComplete(self) -> bool:
        return self.field(FieldNames.IS_NEW_EXPERIMENT.value) or (
            self.field(FieldNames.IS_EXISTING_EXPERIMENT.value)
            and self.field(FieldNames.EXISTING_EXPERIMENT.value) is not None
        )
