from PyQt5 import QtCore
from PyQt5.QtWidgets import  QMainWindow, QStackedWidget, QFileDialog,QTreeWidgetItem
from PyQt5.QtCore import Qt
from itertools import chain

from ime.ui.ui_main_window import Ui_MainWindow
from ime.models import IngestionMetadata, Project, Experiment, Dataset, Datafile
import logging
from ime.widgets.add_files_wizard import AddFilesWizard
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

        self.ui.datasetTreeWidget.itemClicked.connect(self.onClickedDataset)
        self.ui.experimentTreeWidget.itemClicked.connect(self.onClickedExperiment)
        self.ui.projectTreeWidget.itemClicked.connect(self.onClickedProject)
        self.show()

    def onSelectDataset(self, dataset: Dataset):
        # Update property editor with new object
        self.ui.datasetProperties.set_dataset(dataset)


    def onSelectDatafile(self, dataset: Dataset, file_name: str):
        # First, look up the dataset value
        datafile_lookup = [
            datafile
            for datafile in self.metadata.datafiles
            if datafile.dataset_id == dataset.dataset_id
        ]
        if (len(datafile_lookup) != 1):
            logging.warning("Dataset ID %s could not be found or there are" + 
            "more than one entries.", dataset.dataset_id)
        datafile = datafile_lookup[0]
        # Next, look up FileInfo
        fileinfo_lookup = [
            fileinfo
            for fileinfo in datafile.files
            if fileinfo.name == file_name
        ]
        if (len(fileinfo_lookup) != 1):
            logging.warning("Datafile name %s could not be found or there are " + 
            "more than one entries.", file_name)
        fileinfo = fileinfo_lookup[0]
        # Set controls with value
        self.ui.datafileProperties.set_fileinfo(fileinfo)


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

    def reFresh(self,project_info: Project, experiment_info: Experiment, dataset_info: Dataset, datafile_info: Datafile):
        self.metadata.projects.append(project_info)
        self.metadata.experiments.append(experiment_info)
        self.metadata.datasets.append(dataset_info)
        self.metadata.datafiles.append(datafile_info)

        # Calculate dataset size by summing all the files' sizes
        dataset_files = self.metadata.get_files_by_dataset(dataset_info)
        dataset_size = sum([file.size for file in dataset_files])
        # Create tree widget item for the dataset
        # TODO Handle if it's an existing dataset
        l1 = QTreeWidgetItem([dataset_info.dataset_name,file_size_to_str(dataset_size),experiment_info.experiment_name])
        l1.setData(0, QtCore.Qt.ItemDataRole.UserRole, dataset_info)


        # Calculate experiment size by summing all its datasets' sizes
        exp_datasets = self.metadata.get_datasets_by_experiment(experiment_info)
        exp_files = [self.metadata.get_files_by_dataset(dataset) for dataset in exp_datasets]
        exp_size = sum([f.size for f in chain(*exp_files)])
        # Create tree widget item for the experiment
        # TODO Handle if it's an existing experiment
        l2 = QTreeWidgetItem([experiment_info.experiment_name,file_size_to_str(exp_size),project_info.project_name])
        l2.setData(0, QtCore.Qt.ItemDataRole.UserRole, experiment_info)

        # Calculate project size by summing all its experiments' sizes
        proj_exps = self.metadata.get_experiments_by_project(project_info)
        proj_datasets = [self.metadata.get_datasets_by_experiment(exp) for exp in proj_exps]
        proj_files = [self.metadata.get_files_by_dataset(dataset) for dataset in chain(*proj_datasets)]
        proj_size = sum(f.size for f in chain(*proj_files))
        # Create tree widget item for the project
        # TODO Handle if it's an existing project
        l3 = QTreeWidgetItem([project_info.project_name,file_size_to_str(proj_size)])
        l3.setData(0, QtCore.Qt.ItemDataRole.UserRole, project_info)
        

        for file in datafile_info.files:
            file_name = file.name
            file_size = file_size_to_str(file.size)
            l1_child = QTreeWidgetItem([file_name,file_size,""])
            l1_child.setData(0, QtCore.Qt.ItemDataRole.UserRole, file_name)
            l1.addChild(l1_child)
        self.ui.datasetTreeWidget.addTopLevelItem(l1)
        self.ui.experimentTreeWidget.addTopLevelItem(l2)
        self.ui.projectTreeWidget.addTopLevelItem(l3)

    def openWizardWindow(self):  
        model = IngestionMetadataModel(self.metadata)
        self.import_wizard_ui = AddFilesWizard(model)
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()
    
    # Save to yaml files
    def save_to_yaml(self):
        filename = QFileDialog.getSaveFileName(self,"Save File",directory = "test.yaml", initialFilter='Yaml File(*.yaml)')[0]
        if filename:
            with open(filename, 'w') as file:
                file.write(self.metadata.to_yaml())
