from pyexpat import model
import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QStackedWidget, QFileDialog, QTreeWidget,QTreeWidgetItem, QMenu
from PyQt5.QtCore import Qt
from typing import Any, Callable

from ime.ui.ui_main_window import Ui_MainWindow
from ime.models import IngestionMetadata, Project, Experiment, Dataset, Datafile
import logging
from ime.widgets.add_files_wizard import AddFilesWizard, AddFilesWizardResult, AddFilesWizardSkipDataset, AddFilesWizardSkipExperiment, AddFilesWizardSkipProject
from ime.widgets.add_files_wizard_pages_skip import ProjectPage, PExperimentPage, PEDatasetPage
from ime.qt_models import IngestionMetadataModel

# Import the resources file
import default_rc
from .utils import file_size_to_str

class MyTardisMetadataEditor(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

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

        self.ui.datasetTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.datasetTreeWidget.customContextMenuRequested.connect(self.datasetMenuContextTree)
        self.ui.experimentTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.experimentTreeWidget.customContextMenuRequested.connect(self.experimentMenuTreeWidget)
        self.ui.projectTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.projectTreeWidget.customContextMenuRequested.connect(self.projectMenuTreeWidget)
        self.show()
    
    def datasetMenuContextTree(self, point):
        # We build the menu.
        menu = QMenu()
        action = menu.addAction("Add New File...")
        action.triggered.connect(self.openWizardWindowSkipDataset)
        action = menu.addAction("Delete this Dataset")

        menu.exec_(self.ui.datasetTreeWidget.mapToGlobal(point))
    
    def openWizardWindowSkipDataset(self):  
        model = IngestionMetadataModel(self.metadata)
        item = self.ui.datasetTreeWidget.currentItem()
        data = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        # print(data, data.dataset_name, data.experiment_id)
        # To do: create a dic with info about related exp, project
        exp_data = self.experiment_for_dataset(data)
        pro_data = self.project_for_experiment(exp_data)

        self.import_wizard_ui = AddFilesWizardSkipDataset(model,data,exp_data,pro_data)
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()
    
    def deleteItems(self):
        self.ui.datasetTreeWidget.takeTopLevelItem(self.datasetTreeWidget.indexFromItem(self.datasetTreeWidget.currentItem(), 0).row())

    def experimentMenuTreeWidget(self, point):
        index = self.ui.experimentTreeWidget.indexAt(point)

        if not index.isValid():
            return

        #item = self.ui.experimentTreeWidget.itemAt(point)
        item = self.ui.experimentTreeWidget.currentItem()
        exp_selected = item.data(0, Qt.ItemDataRole.UserRole)
        print(exp_selected)
        #name = item.text(0)  # The text of the node.

        # We build the menu.
        menu = QMenu()
        action = menu.addAction("Add New Dataset...")
        action.triggered.connect(self.openWizardWindowSkipExperiment)
        action = menu.addAction("Delete this Experiment")

        menu.exec_(self.ui.experimentTreeWidget.mapToGlobal(point))

    def openWizardWindowSkipExperiment(self):  
        model = IngestionMetadataModel(self.metadata)
        self.import_wizard_ui = AddFilesWizardSkipExperiment(model)
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()

    def projectMenuTreeWidget(self, point):
        index = self.ui.projectTreeWidget.indexAt(point)

        if not index.isValid():
            return

        item = self.ui.projectTreeWidget.itemAt(point)
        name = item.data(0, QtCore.Qt.ItemDataRole.UserRole)

        # We build the menu.
        menu = QMenu()
        action = menu.addAction("Add New Experiment...")
        action.triggered.connect(self.openWizardWindowSkipProject)
        action = menu.addAction("Delete this Project")
        menu.exec_(self.ui.projectTreeWidget.mapToGlobal(point))

    def openWizardWindowSkipProject(self):  
        model = IngestionMetadataModel(self.metadata)
        self.import_wizard_ui = AddFilesWizardSkipProject(model)
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()

    def onSelectDataset(self, dataset: Dataset):
        # Update property editor with new object
        self.ui.datasetProperties.set_dataset(dataset)

    # update with Datafile
    def onSelectDatafile(self, dataset: Dataset, file_name: str):  
        # First, look up the dataset value
        datafiles = self.metadata.get_files_by_dataset(dataset)
        # Next, look up FileInfo
        datafile_lookup = [
            fileinfo
            for fileinfo in datafiles
            if fileinfo.name == file_name
        ]
        if (len(datafile_lookup) != 1):
            logging.warning("Datafile name %s could not be found or there are " + 
            "more than one entries.", file_name)
        fileinfo = datafile_lookup[0]
        # Set controls with value
        self.ui.datafileProperties.set_datafile(fileinfo)  

    def onClickedDataset(self):
            item: QTreeWidgetItem = self.ui.datasetTreeWidget.currentItem()
            item_data = item.data(0, Qt.ItemDataRole.UserRole)
            props_widget : QStackedWidget = self.ui.datasetTabProps
            if item.parent() is None:
                # This indicates we are looking at a dataset,
                # change stacked widget to show dataset properties
                props_widget.setCurrentIndex(0)
                self.onSelectDataset(item_data)
            else:
                parent = item.parent()
                dataset = parent.data(0, Qt.ItemDataRole.UserRole)
                props_widget.setCurrentIndex(1)
                self.onSelectDatafile(dataset, item_data)

    def onClickedExperiment(self):
            item = self.ui.experimentTreeWidget.currentItem()
            exp = item.data(0, Qt.ItemDataRole.UserRole)
            props_widget : QStackedWidget = self.ui.experimentTabProps
            props_widget.setCurrentIndex(0)
            self.ui.expProperties.set_experiment(exp)

    def onClickedProject(self):
            item = self.ui.projectTreeWidget.currentItem()
            project: Project = item.data(0, Qt.ItemDataRole.UserRole)
            props_widget : QStackedWidget = self.ui.projectTabProps
            props_widget.setCurrentIndex(0)
            self.ui.projectProperties.set_project(project)

    def dataset_size(self, dataset: Dataset):
        dataset_files = self.metadata.get_files_by_dataset(dataset)
        return sum([file.size for file in dataset_files])

    def experiment_size(self, exp: Experiment):
        exp_datasets = self.metadata.get_datasets_by_experiment(exp)
        return sum([self.dataset_size(dataset) for dataset in exp_datasets])

    def project_size(self, project: Project):
        proj_exps = self.metadata.get_experiments_by_project(project)
        return sum([self.experiment_size(exp) for exp in proj_exps])
    
    def project_for_experiment(self, experiment: Experiment):
        for project in self.metadata.projects:
            if project.project_id == experiment.project_id:
                return project
        raise ValueError()

    def experiment_for_dataset(self, dataset: Dataset):
        for experiment in self.metadata.experiments:
            if experiment.experiment_id in dataset.experiment_id:
                return experiment
        raise ValueError()

    def dataset_for_datafile(self, datafile: Datafile):
        """Return the Dataset object that corresponds to the given Datafile.
        This method searches for the Dataset object in the metadata attribute of the current object (which should be a class that contains metadata about one or more datasets), 
        by comparing the dataset_id attribute of each Dataset object to the dataset_id attribute of the given Datafile object. If a match is found, the corresponding Dataset object is returned.

        Args:
            datafile: A Datafile object representing the file that we want to find the corresponding Dataset for.
        Returns:
            A Dataset object that corresponds to the given Datafile.
        Raises:
            ValueError: If no Dataset object is found that matches the dataset_id of the given Datafile.
        """
        for dataset in self.metadata.datasets:
            if dataset.dataset_id == datafile.dataset_id:
                return dataset
        raise ValueError()
    

    def find_item_in_tree(self, treeWidget: QTreeWidget, predicate: Callable[[Any],bool]):
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

    def add_project_to_tree(self, project: Project):
        proj_size = file_size_to_str(self.project_size(project))
        l3 = QTreeWidgetItem([project.name,proj_size])
        l3.setData(0, QtCore.Qt.ItemDataRole.UserRole, project)
        self.ui.projectTreeWidget.addTopLevelItem(l3)

    def add_experiment_to_tree(self, experiment: Experiment):
        exp_size = file_size_to_str(self.experiment_size(experiment))
        project = self.project_for_experiment(experiment)
        l2 = QTreeWidgetItem([experiment.title,exp_size,project.name])
        l2.setData(0, QtCore.Qt.ItemDataRole.UserRole, experiment)
        self.ui.experimentTreeWidget.addTopLevelItem(l2)

    def add_dataset_to_tree(self, dataset: Dataset):
        dataset_size = file_size_to_str(self.dataset_size(dataset))
        experiment = self.experiment_for_dataset(dataset)
        ds_item = QTreeWidgetItem([dataset.dataset_name, dataset_size,experiment.title])
        ds_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, dataset)
        self.ui.datasetTreeWidget.addTopLevelItem(ds_item)
    
    ### create new add_datafile_to_tree function
    def add_datafile_to_tree(self, datafile: Datafile):
        """
        Adds a new child item to the QTreeWidget for the dataset that contains the specified Datafile.

        Args:
            datafile (Datafile): The Datafile object to add to the tree.

        Returns:
            None
        """
        ds_item = self.find_item_in_tree(self.ui.datasetTreeWidget, lambda ds: ds.dataset_id == datafile.dataset_id)
        file_name = datafile.name
        file_size = file_size_to_str(datafile.size)
        l1_child = QTreeWidgetItem([file_name,file_size,""])
        l1_child.setData(0, QtCore.Qt.ItemDataRole.UserRole, file_name)
        ds_item.addChild(l1_child)

    def reFresh(self,result: AddFilesWizardResult):
        """
        Method for adding the newly created classes from the wizard into IngestionMetadata,
        and refreshing the project/experiment/dataset/datafile widgets with the new data.
        """
        # Modify IngestionMetadata to insert or modify models
        if result.is_new_dataset:
            self.metadata.datasets.append(result.dataset)
        if result.is_new_project:
            self.metadata.projects.append(result.project)
        if result.is_new_experiment:
            self.metadata.experiments.append(result.experiment)
        self.metadata.datafiles.append(result.datafile)
        # Create tree widget item for the dataset
        ds_item = None
        if result.is_new_dataset:
            self.add_dataset_to_tree(result.dataset)
            # Update experiment and project size.___Libby
        else:
            # Update dataset size.
            dataset_size = file_size_to_str(self.dataset_size(result.dataset))
            ds_item = self.find_item_in_tree(self.ui.datasetTreeWidget, lambda data: (
                data.dataset_id == result.dataset.dataset_id
            ))
            ds_item.setData(1, QtCore.Qt.ItemDataRole.DisplayRole, dataset_size)        
        # Add datafile under dataset
        self.add_datafile_to_tree(result.datafile)
        # Create or tree widget item for the experiment, or find existing and update size.
        if result.is_new_experiment:
            self.add_experiment_to_tree(result.experiment)
        else:
            exp_size = file_size_to_str(self.experiment_size(result.experiment))
            exp_item = self.find_item_in_tree(self.ui.experimentTreeWidget, lambda data:(
                data.experiment_id == result.experiment.experiment_id
            ))
            exp_item.setData(1, QtCore.Qt.ItemDataRole.DisplayRole, exp_size)
        # Create tree widget item for the project, or find existing and update size.
        if result.is_new_project:
            self.add_project_to_tree(result.project)
        else:
            proj_size = file_size_to_str(self.project_size(result.project))
            proj_item = self.find_item_in_tree(self.ui.projectTreeWidget, lambda data:(
                data.project_id == result.project.project_id
            ))
            proj_item.setData(1, QtCore.Qt.ItemDataRole.DisplayRole, proj_size)

    def openWizardWindow(self):  
        model = IngestionMetadataModel(self.metadata)
        self.import_wizard_ui = AddFilesWizard(model)
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()

    # Import metadata from a yaml file
    def loadYaml(self):
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
        with open(fileName) as f:
            data_load = f.read()
            #print(data_load)
            try:
                data_yaml = IngestionMetadata.from_yaml(data_load)
                #print(data_yaml)
                self.display_load_data(data_yaml)
            except Exception as e:
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Error loading file")
                msg_box.setText("There was an error loading the metadata file. Please check to ensure it's valid.")
                msg_box.exec()

    # Display loaded metadata
    def display_load_data(self,data_loaded: IngestionMetadata):
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

    # Save to yaml files
    def save_to_yaml(self):
        filename = QFileDialog.getSaveFileName(self,"Save File",directory = "test.yaml", initialFilter='Yaml File(*.yaml)')[0]
        if filename:
            with open(filename, 'w') as file:
                file.write(self.metadata.to_yaml())
