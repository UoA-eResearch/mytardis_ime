import typing
from PyQt5.QtWidgets import QWizardPage
from ime.widgets.add_files_wizard.enums import FieldNames, PageNames
import ime.widgets.add_files_wizard.wizard as afw

class ProjectPage(QWizardPage):

    def selected_existing_project_changed(self, idx: int) -> None:
        # Look up and record the selected existing project.
        project = self.model.instance(idx)
        self.wizard().selected_existing_project = project

    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        return typing.cast(afw.AddFilesWizard, super().wizard())

    def initializePage(self) -> None:
        wizard = self.wizard()
        # Display the list of projects.
        list_view = wizard.ui.existingProjectList
        self.model = wizard.metadataModel.projects.proxy(['name'])
        self.model.set_read_only(True)
        list_view.setModel(self.model)
        self.selected_existing_project_changed(wizard.ui.existingProjectList.currentIndex())
        list_view.currentIndexChanged.connect(self.selected_existing_project_changed)

    def cleanupPage(self) -> None:
        self.wizard().ui.existingProjectList.currentIndexChanged.disconnect()

    def nextId(self) -> int:
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        if self.field(FieldNames.IS_NEW_PROJECT.value):
            # Go to the new project page
            return wizard.page_ids[PageNames.NEW_PROJECT.value]
        else:
            return wizard.page_ids[PageNames.EXPERIMENT.value]

    def isComplete(self) -> bool:
        # Block Next button until required fields are filled.
        return self.field(FieldNames.IS_NEW_PROJECT.value) or (self.field(FieldNames.IS_EXISTING_PROJECT.value) and self.field(FieldNames.EXISTING_PROJECT.value) is not None)
