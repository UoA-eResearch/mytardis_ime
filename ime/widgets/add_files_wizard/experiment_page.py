import typing
from PyQt5.QtWidgets import QWizardPage
from ime.widgets.add_files_wizard.enums import FieldNames, PageNames
import ime.widgets.add_files_wizard.wizard as afw

class ExperimentPage(QWizardPage):
    def selected_existing_exp_changed(self,idx: int) -> None:
        # Look up and record the selected existing experiment.
        wizard = self.wizard()
        exp = self.model.instance(wizard.ui.existingExperimentList.currentIndex())
        wizard.selected_existing_experiment = exp


    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        wizard = self.wizard()
        # Only show experiments from the selected project.
        project = wizard.selected_existing_project
        assert project is not None
        self.model = wizard.metadataModel.experiments_for_project(project)
        self.model.set_read_only(True)
        self.model.set_show_fields(['title'])
        wizard.ui.existingExperimentList.setModel(self.model)
        self.selected_existing_exp_changed(wizard.ui.existingExperimentList.currentIndex())
        wizard.ui.existingExperimentList.currentIndexChanged.connect(self.selected_existing_exp_changed)

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field(FieldNames.IS_NEW_EXPERIMENT.value):
            # Go to the new project page
            return wizard.page_ids[PageNames.NEW_EXPERIMENT.value]
        else:
            return wizard.page_ids[PageNames.DATASET.value]

    def cleanupPage(self) -> None:
        self.wizard().ui.existingExperimentList.currentIndexChanged.disconnect()

    def isComplete(self) -> bool:
        return self.field(FieldNames.IS_NEW_EXPERIMENT.value) or (self.field(FieldNames.IS_EXISTING_EXPERIMENT.value) and self.field(FieldNames.EXISTING_EXPERIMENT.value) is not None)