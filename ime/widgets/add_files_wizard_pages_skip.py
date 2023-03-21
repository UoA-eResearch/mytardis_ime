"""
add_files_wizard_pages.py - custom logic for add files wizard pages.
"""
import typing
from PyQt5.QtWidgets import QWidget, QWizardPage

from ime.ui.ui_add_files_wizard_skip import Ui_ImportDataFiles
import ime.widgets.add_files_wizard as afw
from ime.qt_models import IngestionMetadataModel
from ime.models import Project, Experiment, Dataset, Datafile
#from ime.mytardismetadataeditor import MyTardisMetadataEditor

class ProjectPage(QWizardPage):
    """ A wizard page for selecting an existing project or creating a new one.

    Args:
        QWizardPage (_type_):  The type of the parent class.
    """
    def selected_existing_project_changed(self,idx):
        # Look up and record the selected existing project.
        """Record the selected existing project.

        Args:
            idx (_type_): _description_
        """
        wizard = self.wizard()
        project = self.model_pro.instance(wizard.ui.existingProjectList_1.currentIndex())
        #project = self.model.instance(idx)
        wizard.selected_existing_project = project

    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        """Return the wizard object with type cast.

        Returns:
            _type_: _description_
        """
        return typing.cast(afw.AddFilesWizardSkipProject, super().wizard())

    def initializePage(self) -> None:
        """Display the list of projects and initialize the selected project."""
        wizard = self.wizard()
        # Display the list of projects.
        list_view = wizard.ui.existingProjectList_1
        self.model_pro = wizard.metadataModel.projects.proxy(['name'])
        self.model_pro.set_read_only(True)
        list_view.setModel(self.model_pro)
        
        self.selected_existing_project_changed(wizard.ui.existingProjectList_1.currentIndex())
        list_view.currentIndexChanged.connect(self.selected_existing_project_changed)

    def cleanupPage(self) -> None:
        """Disconnect the currentIndexChanged signal."""
        self.wizard().ui.existingProjectList_1.currentIndexChanged.disconnect()

    def nextId(self) -> int:
        """Return the id of the next page.

        Returns:
            int: the id of the next page.
        """
        wizard = typing.cast(afw.AddFilesWizard, self.wizard())
        return wizard.page_ids['newExperimentPage']
    
    def isComplete(self) -> bool:
        """Return True if the required fields are filled.

        Returns:
            bool: True if the required fields are filled.
        """
        return self.field('isExistingProject') is not None

class PExperimentPage(QWizardPage):
    """A wizard page for selecting an existing project and experiment or creating a new one."""
    def selected_existing_pe_changed(self,idx):
        """
        Update the list of experiments when the selected project is changed.

        Args:
            idx: The index of the selected project in the project list.
        """
        # Look up and record the selected existing project and experiment.
        wizard = self.wizard()
        idx_current_pro = wizard.ui.existingProjectList_2.currentIndex()
        project = self.model_pro.instance(idx_current_pro)
        self.model_exp = wizard.metadataModel.experiments_for_project(project)
        self.model_exp.set_read_only(True)
        self.model_exp.set_show_fields(['title'])
        wizard.ui.existingExperimentList_1.setModel(self.model_exp)
        exp = self.model_exp.instance(wizard.ui.existingExperimentList_1.currentIndex())

        project = self.model_pro.instance(wizard.ui.existingProjectList_2.currentIndex())
        exp = self.model_exp.instance(wizard.ui.existingExperimentList_1.currentIndex())
        wizard.selected_existing_project = project
        wizard.selected_existing_experiment = exp

    def wizard(self):
        # Add type cast so type checker isn't annoyed below.
        """
        Return the wizard object with type casting.

        Returns:
            The wizard object with type casting.
        """
        return typing.cast(afw.AddFilesWizardSkip, super().wizard())

    def initializePage(self) -> None:
        """
        Initialize the wizard page with a list of projects and experiments.
        """
        wizard = self.wizard()

        list_view_pro = wizard.ui.existingProjectList_2
        list_view_exp = wizard.ui.existingExperimentList_1
        
        # Display the list of projects
        self.model_pro = wizard.metadataModel.projects.proxy(['name'])
        self.model_pro.set_read_only(True)
        list_view_pro.setModel(self.model_pro)

        # Only show experiments from the selected project.
        idx_selected_existing_pro = list_view_pro.currentIndex()
        project = self.model_pro.instance(idx_selected_existing_pro)
        self.model_exp = wizard.metadataModel.experiments_for_project(project)
        self.model_exp.set_read_only(True)
        self.model_exp.set_show_fields(['title'])
        list_view_exp.setModel(self.model_exp)

        #wizard.ui.existingProjectList_2.setModel(self.model)
        self.selected_existing_pe_changed(wizard.ui.existingExperimentList_1.currentIndex())
        list_view_pro.currentIndexChanged.connect(self.selected_existing_pe_changed)
        list_view_exp.currentIndexChanged.connect(self.selected_existing_pe_changed)

    def nextId(self) -> int:
        """
        Return the ID of the next wizard page.

        Returns:
            The ID of the next wizard page.
        """
        wizard = typing.cast(afw.AddFilesWizardSkip, self.wizard())
        return wizard.page_ids['newDatasetPage']

    def cleanupPage(self) -> None:
        """
        Disconnect signals when the wizard page is closed.
        """
        self.wizard().ui.existingExperimentList_1.currentIndexChanged.disconnect()
        self.wizard().ui.existingProjectList_2.currentIndexChanged.disconnect()

    def isComplete(self) -> bool:
        """
        Check if the user has selected an existing project and experiment.

        Returns:
            True if the user has selected an existing project and experiment, False otherwise.
        """
        return self.field('isExistingProject') is not None and self.field('isExistingExperiment') is not None

class PEDatasetPage(QWizardPage):
    """A wizard page for selecting an existing project, experiment, and dataset.

    Args:
        QWizardPage (_type_): The type of the parent class.
    """
    def selected_existing_ped_changed(self, idx):
        """Updates the UI elements with the selected existing project, experiment, and dataset.

        Args:
            idx (int): The index of the current selection.
        """
        wizard = self.wizard()
        
        idx_current_pro = wizard.ui.existingProjectList_3.currentIndex()
        project = self.model_pro.instance(idx_current_pro)
        self.model_exp = wizard.metadataModel.experiments_for_project(project)
        self.model_exp.set_read_only(True)
        self.model_exp.set_show_fields(['title'])
        wizard.ui.existingExperimentList_2.setModel(self.model_exp)

        experiment = self.model_exp.instance(wizard.ui.existingExperimentList_2.currentIndex())
        self.model_ds = wizard.metadataModel.datasets_for_experiment(experiment)
        self.model_ds.set_read_only(True)
        self.model_ds.set_show_fields(['dataset_name'])
        #wizard.ui.existingDatasetList_1.setModel(self.model_ds)

        project = self.model_pro.instance(wizard.ui.existingProjectList_3.currentIndex())
        exp = self.model_exp.instance(wizard.ui.existingExperimentList_2.currentIndex())
        ds = self.model_ds.instance(wizard.ui.existingDatasetList_1.currentIndex())
        
        wizard.selected_existing_project = project
        wizard.selected_existing_experiment = exp
        wizard.selected_existing_dataset = ds
        

    def wizard(self):
        """Returns the wizard object.

        Returns:
            afw.AddFilesWizardSkipDataset: The wizard object.
        """
        return typing.cast(afw.AddFilesWizardSkipDataset, super().wizard())

    def initializePage(self) -> None:
        """Initializes the wizard page."""
        wizard = self.wizard()
        list_view_ds = wizard.ui.existingDatasetList_1
        list_view_exp = wizard.ui.existingExperimentList_2
        list_view_pro = wizard.ui.existingProjectList_3

        self.model_pro = wizard.metadataModel.projects.proxy(['name'])
        self.model_pro.set_read_only(True)
        list_view_pro.setModel(self.model_pro)

        # Only show experiments from the selected project.
        idx_selected_existing_pro = list_view_pro.currentIndex()
        project = self.model_pro.instance(idx_selected_existing_pro)
        
        self.model_exp = wizard.metadataModel.experiments_for_project(project)
        self.model_exp.set_read_only(True)
        self.model_exp.set_show_fields(['title'])
        list_view_exp.setModel(self.model_exp)
        
        ## datasets
        self.model_ds = wizard.metadataModel.datasets.proxy(['dataset_name'])
        self.model_ds.set_read_only(True)
        self.model_ds.set_show_fields(['dataset_name'])
        list_view_ds.setModel(self.model_ds)

        #wizard.ui.existingProjectList_2.setModel(self.model)
        self.selected_existing_ped_changed(wizard.ui.existingProjectList_3.currentIndex())
        list_view_pro.currentIndexChanged.connect(self.selected_existing_ped_changed)


    def cleanupPage(self) -> None:
        """Cleans up the wizard page."""
        self.wizard().ui.existingDatasetList_1.currentIndexChanged.disconnect()
        self.wizard().ui.existingExperimentList_2.currentIndexChanged.disconnect()
        self.wizard().ui.existingProjectList_3.currentIndexChanged.disconnect()

    def nextId(self) -> int:
        """Returns the ID of the next wizard page.

        Returns:
            int: The ID of the next wizard page.
        """
        wizard = typing.cast(afw.AddFilesWizardSkipDataset, self.wizard())
        return wizard.page_ids['includedFilesPage']

    def isComplete(self) -> bool:
        """Checks whether the selection of existing project, experiment, and dataset is complete.

        Returns:
            bool: True if the selection is complete; False otherwise.
        """
        return self.field('isExistingProject') is not None and self.field('isExistingExperiment') is not None and self.field('isExistingDataset') is not None