import logging
import typing
from typing import Any, Callable, cast

import jpype
from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMenu,
    QMessageBox,
    QStackedWidget,
    QTreeWidget,
    QTreeWidgetItem,
)

# Import the resources file
import default_rc
from ime.models import (
    Datafile,
    Dataset,
    DataStatus,
    DifferentDeviceException,
    Experiment,
    IngestionMetadata,
    Project,
)
from ime.qt_models import IngestionMetadataModel
from ime.ui.ui_main_window import Ui_MainWindow
from ime.widgets.add_files_wizard.wizard import AddFilesWizard, AddFilesWizardResult

from .utils import file_size_to_str, setup_section_autoresize


class MyTardisMetadataEditor(QMainWindow):
    """
    A GUI application for editing metadata associated with experimental data files in the MyTardis platform.

    Inherits from QMainWindow.
    """
    def __init__(self):
        """
        Constructor for MyTardisMetadataEditor class.

        Initializes the GUI, sets up the UI widgets, connects UI events to appropriate event handlers, and shows the GUI.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # load the ui file
        # uic.loadUi('MainWindow.ui', self)
        self.metadata = IngestionMetadata()

        # define our widgets
        self.ui.actionImport_data_files.triggered.connect(self.openWizardWindow)
        self.ui.actionSave.triggered.connect(self.save_to_yaml)
        self.ui.actionOpen.triggered.connect(self.loadYaml)

        self.ui.datasetTreeWidget.itemClicked.connect(self.onClickedDataset)
        self.ui.experimentTreeWidget.itemClicked.connect(self.onClickedExperiment)
        self.ui.projectTreeWidget.itemClicked.connect(self.onClickedProject)

        self.ui.datasetTreeWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.datasetTreeWidget.customContextMenuRequested.connect(self.datasetMenuContextTree)
        self.ui.experimentTreeWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.experimentTreeWidget.customContextMenuRequested.connect(self.experimentMenuTreeWidget)
        self.ui.projectTreeWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.projectTreeWidget.customContextMenuRequested.connect(self.projectMenuTreeWidget)

        setup_section_autoresize(self.ui.projectTreeWidget)
        setup_section_autoresize(self.ui.experimentTreeWidget)
        setup_section_autoresize(self.ui.datasetTreeWidget)

        # Prevent context menu that enables hiding toolbar from showing
        self.ui.toolBar.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)

        self.show()

    def closeEvent(self, event):
        # Terminate the JVM when the app is closed
        jpype.shutdownJVM()
        event.accept()

    def openWizardWindow(self) -> None:  
        """
        Displays a wizard window to add new files to an existing experiment. 
        This method extracts the relevant metadata from the currently selected item in the 
        experiment tree widget and passes it to the AddFilesWizardSkipExperiment object.

        Args: None

        Returns: None
        """
        model = IngestionMetadataModel(self.metadata)
        self.import_wizard_ui = AddFilesWizard(model)
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()

    def datasetMenuContextTree(self, point) -> None:
        """
        Event handler for the context menu triggered in the datasetTreeWidget.

        Builds the context menu and connects its actions to appropriate event handlers. Shows the context menu at the
        specified point.

        :param point: QPoint representing the position where the context menu was triggered.
        """
        index = self.ui.datasetTreeWidget.indexAt(point)
        item = self.ui.datasetTreeWidget.itemAt(point)
        if item is None:
            return
        menu = QMenu()
        if not index.isValid() or index.parent().isValid(): # if the item is not a dataset
            delete_action = menu.addAction("Remove this File")
            file: Datafile = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
            if file.data_status == DataStatus.INGESTED.value:
                delete_action.setEnabled(False)
            else:
                delete_action.triggered.connect(self.delete_items_datafile)        
        else:
            dataset: Dataset = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
            action = menu.addAction("Add New Files...")
            action.triggered.connect(self.openWizardWindowSkipDataset)
            delete_action = menu.addAction("Remove this Dataset")
            # disable delete action if dataset has been ingested in MyTardis
            if dataset.data_status == DataStatus.INGESTED.value:
                delete_action.setEnabled(False)  
            else:
                delete_action.triggered.connect(self.delete_items_dataset)
        menu.exec(self.ui.datasetTreeWidget.mapToGlobal(point))     

    def openWizardWindowSkipDataset (self) -> None:
        """
        Event handler for the "Add New File..." action triggered in the context menu of the datasetTreeWidget.

        Initializes the AddFilesWizardSkipDataset UI and shows it to the user. Connects the submitted event of the UI
        to the reFresh event handler.

        Args: None

        Returns: None
        """  
        model = IngestionMetadataModel(self.metadata)
        item = self.ui.datasetTreeWidget.currentItem()
        ds_data = cast(Dataset, item.data(0, QtCore.Qt.ItemDataRole.UserRole))
        # To do: create a dic with info about related exp, project
        exp_data = self.experiment_for_dataset(ds_data)
        pro_data = self.project_for_experiment(exp_data)

        self.import_wizard_ui = AddFilesWizard(model, pro_data, exp_data, ds_data)
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()

    def delete_items_dataset(self) -> None:
        """
        Deletes the selected dataset and its associated files from the dataset tree.

        This function prompts the user for confirmation before deleting the dataset.
        If the user confirms, the dataset and its associated files are removed from the dataset tree.

        Note: The dataset and its associated files are also removed from the metadata.

        Returns:
            None
        """
        selected_item = self.ui.datasetTreeWidget.currentItem() ## it's the Dataset

        if not selected_item:
            return
        confirm_msg = QMessageBox()
        confirm_msg.setWindowTitle("Remove this dataset?")
        confirm_msg.setText('Remove this dataset?')
        confirm_msg.setInformativeText("Metadata you've entered will also be removed. Files in this dataset will be kept on your drive.")
        confirm_msg.setStandardButtons(typing.cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel))
        res = confirm_msg.exec()
        if res == QMessageBox.StandardButton.Cancel:
            # If user did not want to proceed, then exit.
            return
        # Remove dataset from the tree
        self.ui.datasetTreeWidget.takeTopLevelItem(self.ui.datasetTreeWidget.indexOfTopLevelItem(selected_item))
        datafiles_impacted = self.metadata.get_files_by_dataset(selected_item.data(0, QtCore.Qt.ItemDataRole.UserRole))
        self.metadata.datasets.remove(selected_item.data(0, QtCore.Qt.ItemDataRole.UserRole))
        for file in datafiles_impacted:
            self.metadata.datafiles.remove(file)
        # Finally, change property editor to no longer show dataset properties.
        self.ui.datasetTabProps.setCurrentIndex(2)
        self.ui.datasetTreeWidget.clearSelection()

    def delete_items_datafile(self) -> None:
        """
        Deletes the selected data file from the dataset tree.

        This function prompts the user for confirmation before deleting the data file.
        If the user confirms, the data file is removed from the dataset tree and metadata.

        Args: None

        Returns: None
        """
        selected_item = self.ui.datasetTreeWidget.currentItem() ### it's the file name
        if selected_item:
            confirm_msg = QMessageBox()
            confirm_msg.setWindowTitle("Remove this file?")
            confirm_msg.setText('Remove this file?')
            confirm_msg.setInformativeText("Metadata you've entered or extracted will also be removed. The file will be kept on your drive.")
            confirm_msg.setStandardButtons(typing.cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel))
            res = confirm_msg.exec()
            if res == QMessageBox.StandardButton.Cancel:
                # If user did not want to proceed, then exit.
                return
            datafile: Datafile = selected_item.data(0, QtCore.Qt.ItemDataRole.UserRole)
            if datafile:
                # Remove the datafile from the tree
                self.metadata.datafiles.remove(datafile)

            # Remove the selected item from the tree
            index = self.ui.datasetTreeWidget.indexOfTopLevelItem(selected_item)
            if index != -1:
                self.ui.datasetTreeWidget.takeTopLevelItem(index)
            else:
                parent = selected_item.parent()
                if parent:
                    parent.removeChild(selected_item)
            # Change property editor to no longer show datafile properties
            self.ui.datasetTabProps.setCurrentIndex(2)
            self.ui.datasetTreeWidget.clearSelection()

    def experimentMenuTreeWidget(self, point) -> None:
        """
        Displays a context menu with the option to add a new dataset to the selected experiment.
        If a valid experiment item is not selected, the menu is not displayed.

        Args:
            - point: QPoint object indicating the position where the context menu was requested.

        Returns: None
        """
        index = self.ui.experimentTreeWidget.indexAt(point)
        item = self.ui.experimentTreeWidget.itemAt(point)
        if item is None:
            return
        item_data = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        # We build the menu.
        menu = QMenu()
        action = menu.addAction("Add New Dataset...")
        action.triggered.connect(self.openWizardWindowSkipExperiment)
        delete_action = menu.addAction("Delete this Experiment")
        if item_data.data_status == DataStatus.INGESTED.value:
            delete_action.setEnabled(False)
        else:
            delete_action.triggered.connect(self.delete_items_experiment)
        menu.exec_(self.ui.experimentTreeWidget.mapToGlobal(point))

    def delete_items_experiment(self) -> None:
        """
        Event handler for the "Delete this Experiment" action triggered in the context menu of the experimentTreeWidget.
        Deletes the selected experiment and its associated datasets and data files from the experimentTreeWidget and metadata.

        Args: None

        Returns: None
        """
        selected_item = self.ui.experimentTreeWidget.currentItem() ## it's the Experiment
        if not selected_item:
            return
        confirm_msg = QMessageBox()
        confirm_msg.setWindowTitle("Remove this experiment?")
        confirm_msg.setText('Remove this experiment?')
        confirm_msg.setInformativeText("Metadata you've entered will also be removed. Files in this experiment will be kept on your drive.")
        confirm_msg.setStandardButtons(typing.cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel))
        res = confirm_msg.exec()
        if res == QMessageBox.StandardButton.Cancel:
            # If user did not want to proceed, then exit.
            return
        self.ui.experimentTreeWidget.takeTopLevelItem(self.ui.experimentTreeWidget.indexOfTopLevelItem(selected_item))
        experiment = selected_item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        datasets_impacted = self.metadata.get_datasets_by_experiment(experiment)

        datafiles_impacted = [] # the full list of datafiles impacted by the deletion of the datasets
        for dataset in datasets_impacted:
            datafiles_related = self.metadata.get_files_by_dataset(dataset)
            datafiles_impacted.extend(datafiles_related)
            self.metadata.datasets.remove(dataset)

        self.metadata.experiments.remove(selected_item.data(0, QtCore.Qt.ItemDataRole.UserRole))

        for file in datafiles_impacted:
            self.metadata.datafiles.remove(file)

        # clear the dataset tree widget and repopulate it with the remaining datasets/datafiles
        self.ui.datasetTreeWidget.clear()
        for ds in self.metadata.datasets:
            self.add_dataset_to_tree(ds)

        # Build a list of all dataset identifiers
        ds_id = []
        for ds in self.metadata.datasets:
            ds_id += ds.identifiers

        for file in self.metadata.datafiles:
            if file.dataset in ds_id: 
                self.add_datafile_to_tree(file)
            else:
                pass
        # Finally, change property editor to no longer show dataset properties.
        self.ui.experimentTabProps.setCurrentIndex(1)
        self.ui.datasetTabProps.setCurrentIndex(2)
        self.ui.experimentTreeWidget.clearSelection()
        self.ui.datasetTreeWidget.clearSelection()

    def openWizardWindowSkipExperiment(self) -> None:
        """
        Displays a wizard window to add new files to an existing experiment. 
        This method extracts the relevant metadata from the currently selected item in the 
        experiment tree widget and passes it to the AddFilesWizardSkipExperiment object.

        Args: None

        Returns: None
        """
        model = IngestionMetadataModel(self.metadata)
        item = self.ui.experimentTreeWidget.currentItem()
        exp_data = cast(Experiment, item.data(0, QtCore.Qt.ItemDataRole.UserRole))
        pro_data = self.project_for_experiment(exp_data)

        self.import_wizard_ui = AddFilesWizard(model,pro_data, exp_data)
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()

    def projectMenuTreeWidget(self, point) -> None:
        """
        Displays a context menu with the option to add a new experiment to the selected project.
        If a valid project item is not selected, the menu is not displayed.

        Args:
        - point: QPoint object indicating the position where the context menu was requested.

        Returns: None
        """    
        # We build the menu.
        index = self.ui.projectTreeWidget.indexAt(point)
        item = self.ui.projectTreeWidget.itemAt(point)
        if item is None:
            return
        item_data = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        # We build the menu.
        menu = QMenu()
        action = menu.addAction("Add New Experiment...")
        action.triggered.connect(self.openWizardWindowSkipProject)
        delete_action = menu.addAction("Delete this Project")
        if item_data.data_status == DataStatus.INGESTED.value:
            delete_action.setEnabled(False)
        else:
            delete_action.triggered.connect(self.delete_items_project)
        menu.exec(self.ui.projectTreeWidget.mapToGlobal(point))

    def delete_items_project(self) -> None:
        """
        Event handler for the "Delete this Project" action triggered in the context menu of the projectTreeWidget.
        Deletes the selected project and its associated experiments, datasets, and data files from the projectTreeWidget and metadata.

        Args: None

        Returns: None
        """
        selected_item = self.ui.projectTreeWidget.currentItem()
        if not selected_item:
            return
        confirm_msg = QMessageBox()
        confirm_msg.setWindowTitle("Remove this project?")
        confirm_msg.setText('Remove this project?')
        confirm_msg.setInformativeText("Metadata you've entered will also be removed. Files in this project will be kept on your drive.")
        confirm_msg.setStandardButtons(typing.cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel))
        res = confirm_msg.exec()
        if res == QMessageBox.StandardButton.Cancel:
            # If user did not want to proceed, then exit.
            return
        self.ui.projectTreeWidget.takeTopLevelItem(self.ui.projectTreeWidget.indexOfTopLevelItem(selected_item)) # remove the project from the project tree widget
        # get the experiments and datasets impacted by the deletion of the project
        project = selected_item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        experiments_impacted = self.metadata.get_experiments_by_project(project)
        datasets_impacted = [] # the full list of datasets impacted by the deletion of the experiments
        for experiment in experiments_impacted:
            dataset_related = self.metadata.get_datasets_by_experiment(experiment)
            datasets_impacted.extend(dataset_related)
            self.metadata.experiments.remove(experiment)

        datafiles_impacted = [] # the full list of datafiles impacted by the deletion of the datasets
        for dataset in datasets_impacted:
            datafiles_related = self.metadata.get_files_by_dataset(dataset)
            datafiles_impacted.extend(datafiles_related)
            self.metadata.datasets.remove(dataset)

        # remove the experiment from the metadata
        self.metadata.projects.remove(project)

        # remove the datafiles impacted by the deletion of the project from the metadata
        for file in datafiles_impacted:
            self.metadata.datafiles.remove(file)

        # repopulate the experiment tree widget with the remaining experiments after metadata is ready
        self.ui.experimentTreeWidget.clear()
        for exp in self.metadata.experiments:
            self.add_experiment_to_tree(exp)

        self.ui.datasetTreeWidget.clear()
        for ds in self.metadata.datasets:
            self.add_dataset_to_tree(ds)

        # clear the datafile tree widget and repopulate it with the remaining datafiles
        # Build a list of all dataset identifiers
        ds_id = []
        for ds in self.metadata.datasets:
            ds_id += ds.identifiers

        for file in self.metadata.datafiles:
            if file.dataset in ds_id: 
                self.add_datafile_to_tree(file)
            else:
                pass
        # Finally, change property editor to no longer show dataset properties.
        self.ui.projectTabProps.setCurrentIndex(1)
        self.ui.experimentTabProps.setCurrentIndex(1)
        self.ui.datasetTabProps.setCurrentIndex(2)
        self.ui.projectTreeWidget.clearSelection()
        self.ui.experimentTreeWidget.clearSelection()
        self.ui.datasetTreeWidget.clearSelection()

    def openWizardWindowSkipProject(self) -> None:
        """
        Displays a wizard window to add new files to a new experiment in an existing project.
        This method extracts the relevant metadata from the currently selected item in the 
        project tree widget and passes it to the AddFilesWizardSkipProject object.

        Args: None

        Returns: None
        """
        model = IngestionMetadataModel(self.metadata)
        item = self.ui.projectTreeWidget.currentItem()
        pro_data = item.data(0, QtCore.Qt.ItemDataRole.UserRole)

        self.import_wizard_ui = AddFilesWizard(model,pro_data)
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()

    def onSelectDataset(self, dataset: Dataset) -> None:
        """
        Updates the property editor with the properties of the selected dataset.

        Args:
            dataset: A Dataset object representing the selected dataset.
        """
        self.ui.datasetProperties.set_dataset(dataset)

    def onSelectDatafile(self, file: Datafile) -> None:  
        """
        Updates the property editor with the properties of the selected datafile.

        Args:
            file: The Datafile object representing the selected datafile.
        """
        self.ui.datafileProperties.set_datafile(file)  

    def onClickedDataset(self) -> None:
        """
        Handles the click event on the dataset tree widget, updates the property editor accordingly.
        """
        item: QTreeWidgetItem = self.ui.datasetTreeWidget.currentItem()
        props_widget : QStackedWidget = self.ui.datasetTabProps
        if item.parent() is None:
            item_data: Dataset = item.data(0, Qt.ItemDataRole.UserRole)
            # This indicates we are looking at a dataset,
            # change stacked widget to show dataset properties
            props_widget.setCurrentIndex(0)
            self.onSelectDataset(item_data)
        else:
            # this indicates we are looking at a datafile
            datafile: Datafile = item.data(0, Qt.ItemDataRole.UserRole)
            props_widget.setCurrentIndex(1)
            self.onSelectDatafile(datafile)

    def onClickedExperiment(self) -> None:
        """
        Handles the click event on the experiment tree widget, updates the property editor accordingly.
        """
        item = self.ui.experimentTreeWidget.currentItem()
        exp = item.data(0, Qt.ItemDataRole.UserRole)
        props_widget : QStackedWidget = self.ui.experimentTabProps
        props_widget.setCurrentIndex(0)
        self.ui.expProperties.set_experiment(exp)

    def onClickedProject(self) -> None:
        """
        Handles the click event on the project tree widget, updates the property editor accordingly.
        """
        item = self.ui.projectTreeWidget.currentItem()
        project: Project = item.data(0, Qt.ItemDataRole.UserRole)
        props_widget : QStackedWidget = self.ui.projectTabProps
        props_widget.setCurrentIndex(0)
        self.ui.projectProperties.set_project(project)

    def dataset_size(self, dataset: Dataset) -> int:
        """
        Computes the total size of the files in the given dataset.

        Args:
            dataset (Dataset): A `Dataset` object representing the dataset.

        Returns:
            int: An integer representing the total size of the files in bytes.
        """
        dataset_files = self.metadata.get_files_by_dataset(dataset)
        sizes = [int(file.size) for file in dataset_files]
        return sum(sizes)

    def experiment_size(self, exp: Experiment) -> int:
        """
        Computes the total size of the files in all datasets of the given experiment.

        Args:
        - exp: An `Experiment` object representing the experiment.

        Returns:
        - An integer representing the total size of the files in bytes.
        """
        exp_datasets = self.metadata.get_datasets_by_experiment(exp)
        return sum([self.dataset_size(dataset) for dataset in exp_datasets])

    def project_size(self, project: Project) -> int:
        """
        Computes the total size of the files in all experiments and datasets of the given project.

        Args:
        - project: A `Project` object representing the project.

        Returns:
        - An integer representing the total size of the files in bytes.
        """
        proj_exps = self.metadata.get_experiments_by_project(project)
        return sum([self.experiment_size(exp) for exp in proj_exps])

    def project_for_experiment(self, experiment: Experiment) -> Project:
        """
        Retrieves the project object that the given experiment belongs to.

        Args:
        - experiment: An `Experiment` object representing the experiment.

        Returns:
        - A `Project` object representing the project.
    
        Raises:
        - ValueError: If the experiment does not belong to any project.
        """
        for project in self.metadata.projects:
            if project.identifiers_delegate.has(experiment.projects):
                return project
        raise ValueError()

    def experiment_for_dataset(self, dataset: Dataset) -> Experiment:
        """
        Retrieves the experiment object that the given dataset belongs to.

        Args:
        - dataset: A `Dataset` object representing the dataset.

        Returns:
        - An `Experiment` object representing the experiment.

        Raises:
        - ValueError: If the dataset does not belong to any experiment.
        """
        for experiment in self.metadata.experiments:
            if experiment.identifiers_delegate.has(dataset.experiments):
                return experiment
        raise ValueError()

    def dataset_for_datafile(self, datafile: Datafile) -> Dataset:
        """Return the Dataset object that corresponds to the given Datafile.
        This method searches for the Dataset object in the metadata attribute of the current object (which should be a class that contains metadata about one or more datasets), 
        by comparing the dataset_id attribute of each Dataset object to the dataset attribute of the given Datafile object. If a match is found, the corresponding Dataset object is returned.

        Args:
            datafile: A Datafile object representing the file that we want to find the corresponding Dataset for.
        Returns:
            A Dataset object that corresponds to the given Datafile.
        Raises:
            ValueError: If no Dataset object is found that matches the dataset of the given Datafile.
        """
        for dataset in self.metadata.datasets:
            if dataset.identifiers_delegate.has(datafile.dataset):
                return dataset
        raise ValueError()

    def find_item_in_tree(self, treeWidget: QTreeWidget, predicate: Callable[[Any],bool]) -> QTreeWidgetItem:
        """
        Finds and returns the first top-level item in the specified QTreeWidget for which the given predicate function returns True.

        Args:
            treeWidget (QTreeWidget): The QTreeWidget to search for items in.
            predicate (Callable[[Any],bool]): A callable that takes an item's data as input and returns a boolean indicating whether the item meets the search criteria.

        Returns:
            QTreeWidgetItem: The first top-level item in the treeWidget that satisfies the search criteria.

        Raises:
            Exception: If no items in the treeWidget satisfy the search criteria.
        """
        count = treeWidget.topLevelItemCount()
        for i in range(0, count):
            item = treeWidget.topLevelItem(i)
            data = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
            if predicate(data):
                return item
        raise Exception("Could not find item in tree.")

    def add_project_to_tree(self, project: Project) -> None:
        """
        Adds a project to the project tree widget.
        Args:
            project (Project): The project object to be added to the tree.
        """
        proj_size = file_size_to_str(self.project_size(project))
        l3 = QTreeWidgetItem([project.name,proj_size])
        l3.setData(0, QtCore.Qt.ItemDataRole.UserRole, project)
        self.ui.projectTreeWidget.addTopLevelItem(l3)

    def add_experiment_to_tree(self, experiment: Experiment) -> None:
        """
        Adds an experiment to the experiment tree widget.
        Args:
            experiment (Experiment): The experiment object to be added to the tree.
        """
        exp_size = file_size_to_str(self.experiment_size(experiment))
        project = self.project_for_experiment(experiment)
        l2 = QTreeWidgetItem([experiment.title,exp_size,project.name])
        l2.setData(0, QtCore.Qt.ItemDataRole.UserRole, experiment)
        self.ui.experimentTreeWidget.addTopLevelItem(l2)

    def add_dataset_to_tree(self, dataset: Dataset) -> None:
        """
        Adds a dataset to the dataset tree widget.
        
        Args:
            dataset (Dataset): The dataset object to be added to the tree.
        """
        dataset_size = file_size_to_str(self.dataset_size(dataset))
        experiment = self.experiment_for_dataset(dataset)
        ds_item = QTreeWidgetItem([dataset.description, dataset_size,experiment.title])
        ds_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, dataset)
        self.ui.datasetTreeWidget.addTopLevelItem(ds_item)

    def add_datafile_to_tree(self, datafile: Datafile) -> None:
        """
        Adds a new child item to the QTreeWidget for the dataset that contains the specified Datafile.

        Args:
            datafile (Datafile): The Datafile object to add to the tree.

        Returns:
            None
        """
        ds_item = self.find_item_in_tree(self.ui.datasetTreeWidget, lambda ds: 
            cast(Dataset, ds).identifiers_delegate.has(datafile.dataset)
        )
        file_name = datafile.filename
        file_size = file_size_to_str(datafile.size)
        l1_child = QTreeWidgetItem([file_name,file_size,""])
        l1_child.setData(0, QtCore.Qt.ItemDataRole.UserRole, datafile)
        ds_item.addChild(l1_child)

    def reFresh(self,result: AddFilesWizardResult) -> None:
        """
        Method for adding the newly created classes from the wizard into IngestionMetadata,
        and refreshing the project/experiment/dataset/datafile widgets with the new data.

        Args:
            result: Resulting object from add files wizard.
        """
        # Modify IngestionMetadata to insert or modify models
        if result.is_new_dataset:
            result.dataset._store = self.metadata
            self.metadata.datasets.append(result.dataset)
        if result.is_new_project:
            result.project._store = self.metadata
            self.metadata.projects.append(result.project)
        if result.is_new_experiment:
            result.experiment._store = self.metadata
            self.metadata.experiments.append(result.experiment)
        for new_file in result.file_list:
            new_file._store = self.metadata
            self.metadata.datafiles.append(new_file)
        # Create tree widget item for the dataset
        ds_item = None
        if result.is_new_dataset:
            self.add_dataset_to_tree(result.dataset)
            # Update experiment and project size.___Libby
        else:
            # Update dataset size.
            dataset_size = file_size_to_str(self.dataset_size(result.dataset))
            ds_item = self.find_item_in_tree(self.ui.datasetTreeWidget, lambda data: (
                result.dataset.identifiers_delegate.has(cast(Dataset, data).identifiers or [])
            ))
            ds_item.setData(1, QtCore.Qt.ItemDataRole.DisplayRole, dataset_size)        
        # Add datafile under dataset
        for new_file in result.file_list:
            self.add_datafile_to_tree(new_file)
        # Create or tree widget item for the experiment, or find existing and update size.
        if result.is_new_experiment:
            self.add_experiment_to_tree(result.experiment)
        else:
            exp_size = file_size_to_str(self.experiment_size(result.experiment))
            exp_item = self.find_item_in_tree(self.ui.experimentTreeWidget, lambda data:(
                result.experiment.identifiers_delegate.has(cast(Experiment, data).identifiers or [])
            ))
            exp_item.setData(1, QtCore.Qt.ItemDataRole.DisplayRole, exp_size)
        # Create tree widget item for the project, or find existing and update size.
        if result.is_new_project:
            self.add_project_to_tree(result.project)
        else:
            proj_size = file_size_to_str(self.project_size(result.project))
            proj_item = self.find_item_in_tree(self.ui.projectTreeWidget, lambda data:(
                cast(Project, data).identifiers_delegate.has(result.project.identifiers or [])
            ))
            proj_item.setData(1, QtCore.Qt.ItemDataRole.DisplayRole, proj_size)

    def loadYaml(self) -> None:
        """
        Loads metadata from a YAML file. If there are unsaved changes in the current metadata, it prompts the user to
        confirm whether they want to discard those changes and open the new file. If the user cancels, it does nothing.
        Otherwise, it loads the metadata from the selected file and displays it in the GUI. If there is an error
        loading the file, it displays an error message.
        """
        if not self.metadata.is_empty():
            # Check user is OK with opening another file
            confirm_msg = QMessageBox()
            confirm_msg.setWindowTitle("Open another file?")
            confirm_msg.setText('Discard unsaved changes and open another file?')
            confirm_msg.setInformativeText("Unsaved changes in the current file will be lost.")
            confirm_msg.setStandardButtons(typing.cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel))
            res = confirm_msg.exec()
            if res == QMessageBox.StandardButton.Cancel:
                # If user did not want to proceed, then exit.
                return
        fileName = QFileDialog.getOpenFileName(self, "Open File",'', "Yaml(*.yaml);;AllFiles(*.*)")[0]
        if fileName == '':
            # If user dismissed the Open File dialog, then exit.
            return
        try:
            data_yaml = IngestionMetadata.from_file(fileName)
            self.display_load_data(data_yaml)
        except Exception as e:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Error loading file")
            msg_box.setText("There was an error loading the metadata file. Please check to ensure it's valid.")
            msg_box.exec()
            self.display_load_data(IngestionMetadata())

    def display_load_data(self,data_loaded: IngestionMetadata) -> None:
        """
        Displays the loaded metadata in the GUI. It clears the existing metadata, then adds the loaded metadata to the
        appropriate tree widgets.

        Args:
            data_loaded (IngestedMetadata): The ingestion metadata to display.
        """
        # Clear existing metadata.
        self.metadata = data_loaded
        self.ui.projectTreeWidget.clear()
        self.ui.experimentTreeWidget.clear()
        self.ui.datasetTreeWidget.clear()
        # self.metadata.projects += data_loaded.projects
        # self.metadata.experiments += data_loaded.experiments
        # self.metadata.datasets += data_loaded.datasets
        # self.metadata.datafiles += data_loaded.datafiles

        # Add loaded metadata to the tree widgets.
        for pro in data_loaded.projects:
            self.add_project_to_tree(pro)
        for exp in data_loaded.experiments:
            self.add_experiment_to_tree(exp)
        for ds in data_loaded.datasets:
            self.add_dataset_to_tree(ds)
        for file in data_loaded.datafiles:
            self.add_datafile_to_tree(file)

    def save_to_yaml(self) -> None:
        """
        Saves the metadata to a YAML file. It prompts the user to select a file name and location, then writes the metadata
        to the selected file.
        """
        while True:
            filename = QFileDialog.getSaveFileName(self,"Save ingestion file",dir = "ingestion.yaml", filter='Yaml File(*.yaml)')[0]
            if filename == "":
                # If the user cancelled and did not provide a filename, then do nothing.
                return
            try:
                self.metadata.to_file(filename)
                break
            except DifferentDeviceException:
                # User is trying to save ingestion file into a different device.
                # Reject and ask if they want to try another path.
                drive_msg = "the same drive" 
                if self.metadata.file_path is not None:
                    drive = self.metadata.file_path.drive
                    if drive != "":
                        drive_msg = f"the {drive} drive"
                retry_msg = QMessageBox()
                retry_msg.setWindowTitle("Can't save ingestion file in this location")
                retry_msg.setText("Please save the ingestion file in the same drive as your data.")
                retry_msg.setInformativeText(f'The ingestion file needs to be saved in the same mapped drive as your data in order to be found by the ingestion process. Please save the ingestion file in {drive_msg}.')
                retry_msg.setStandardButtons(
                    typing.cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel))
                res = retry_msg.exec()
                if res == QMessageBox.StandardButton.Cancel:
                    # If user did not want to proceed, then exit.
                    break
                if res == QMessageBox.StandardButton.Retry:
                    # If retrying, restart the loop.
                    continue
            except Exception as e:
                logging.error(e)
                error_msg = QMessageBox()
                error_msg.setWindowTitle("Can't save ingestion file")
                error_msg.setText("An error occurred when saving the ingestion file.")
                error_msg.setInformativeText("Please try again later.")
                error_msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                error_msg.exec()
                break
