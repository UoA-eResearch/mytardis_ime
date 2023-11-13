
import typing
from ime.widgets.add_files_wizard.enums import FieldNames, PageNames
import ime.widgets.add_files_wizard.wizard as afw
from PyQt6.QtWidgets import QWizardPage

class DatasetPage(QWizardPage):
    def selected_existing_dataset_changed(self, idx: int) -> None:
        # Look up and record the selected existing dataset.
        ds = self.model.instance(idx)
        self.wizard().selected_existing_dataset = ds

    def wizard(self):
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        wizard = self.wizard()
        exp = wizard.selected_existing_experiment
        # Only show datasets under the selected experiment.
        assert exp is not None
        self.model = wizard.metadataModel.datasets_for_experiment(exp)
        self.model.set_read_only(True)
        self.model.set_show_fields(['description'])
        wizard.ui.existingDatasetList.setModel(self.model)
        self.selected_existing_dataset_changed(wizard.ui.existingDatasetList.currentIndex())
        wizard.ui.existingDatasetList.currentIndexChanged.connect(self.selected_existing_dataset_changed)

    def cleanupPage(self) -> None:
        self.wizard().ui.existingDatasetList.currentIndexChanged.disconnect()

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field(FieldNames.IS_NEW_DATASET.value):
            # Go to the new project page
            return wizard.page_ids[PageNames.NEW_DATASET.value]
        else:
            return wizard.page_ids[PageNames.INCLUDED_FILES.value]

    def isComplete(self) -> bool:
        return self.field(FieldNames.IS_NEW_DATASET.value) or (self.field(FieldNames.IS_EXISTING_DATASET.value) and self.field(FieldNames.EXISTING_DATASET.value) is not None)
