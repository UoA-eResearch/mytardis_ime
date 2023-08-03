import typing
from PyQt5.QtWidgets import QWizardPage
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
        if self.field('isNewProject'):
            # Go to the new project page
            return wizard.page_ids['newProjectPage']
        else:
            return wizard.page_ids['experimentPage']

    def isComplete(self) -> bool:
        # Block Next button until required fields are filled.
        return self.field('isNewProject') or (self.field('isExistingProject') and self.field('existingProject') is not None)
