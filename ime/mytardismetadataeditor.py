import os, sys
from typing import List
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QToolBar, QAction, QWizard, QTableWidget, QTableWidgetItem, QLineEdit,QWizardPage, QVBoxLayout, QLabel,QFileDialog, QTreeWidget,QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from isort import file
from itertools import chain

from .ui.MainWindow import Ui_MainWindow
from .ui.AddFilesWizard import Ui_ImportDataFiles
from .models import IngestionMetadata, Project, Experiment, Dataset, Datafile, FileInfo
import logging
# Import the resources file
import default_rc

def file_size_to_str(size: float) -> str:
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0
        # If size exceeds 1024 TB, return in terms of TB.
        return "%3.1f %s" % (size, "TB")

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
        self.import_wizard_ui = WindowWizard()
        self.import_wizard_ui.submitted.connect(self.reFresh)
        self.import_wizard_ui.show()
    
    # Save to yaml files
    def save_to_yaml(self):
        filename = QFileDialog.getSaveFileName(self,"Save File",directory = "test.yaml", initialFilter='Yaml File(*.yaml)')[0]
        if filename:
            with open(filename, 'w') as file:
                file.write(self.metadata.to_yaml())

class WindowWizard(QWizard):

    submitted = QtCore.pyqtSignal(Project, Experiment, Dataset, Datafile)

    def _register_fields(self):
        proj_page = self.ui.wizardPage1
        proj_page.registerField("projectIDLineEdit*", self.ui.projectIDLineEdit)
        proj_page.registerField("projectNameLineEdit*", self.ui.projectNameLineEdit)
        exp_page = self.ui.wizardPage2
        exp_page.registerField("experimentNameLineEdit*", self.ui.experimentNameLineEdit)
        exp_page.registerField("experimentIDLineEdit*", self.ui.experimentIDLineEdit)
        ds_page = self.ui.datasetInfo
        # ds_page.registerField("")

    def __init__(self):
        super(QWizard, self).__init__()
        self.ui = Ui_ImportDataFiles()
        self.ui.setupUi(self)
        self._register_fields()
        # define out widgets
        self.ui.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        self.ui.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_submit)

    def addFiles_handler(self):
        table = self.ui.datafiletableWidget
        files_to_add = self.open_add_files_dialog()
        self.add_file_table_rows(table,files_to_add)

    def deleteFiles_handler(self):
        index_list = []
        for model_index in self.ui.datafiletableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.ui.datafiletableWidget.removeRow(index.row())

    # calculate sizes of added datafiles in bytes,KB,MB,GB,TB

    def open_add_files_dialog(self) -> List[QtCore.QFileInfo]:
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        filename = file_dialog.getOpenFileNames(self, "Open files")  
        fpath = filename[0]

        new_files = []
        for f in fpath:
            if f == "":
                continue
            info = QtCore.QFileInfo(f)
            if info in new_files:
                continue
            new_files.append(info)
        return new_files
    
    def add_file_table_rows(self,table: QTableWidget,files_to_add: List[QtCore.QFileInfo]) -> None:
        # Need to start inserting rows after existing rows.
        initial_row_count = table.rowCount()
        # Grow the table to fit new rows.
        table.setRowCount(initial_row_count + len(files_to_add))
        new_row_index = 0
        for file in files_to_add:
            # Create corresponding cells for file and insert them into table.
            name_cell = QTableWidgetItem(file.fileName())
            size = file.size()
            size_str = file_size_to_str(size)
            size_cell = QTableWidgetItem(size_str)
            # Store actual size value in cell. 
            size_cell.setData(QtCore.Qt.ItemDataRole.UserRole, size)
            fpath_cell = QTableWidgetItem(file.filePath())
            # Insert cells into the table.
            row_index = initial_row_count + new_row_index
            table.setItem(row_index, 0, name_cell)
            table.setItem(row_index, 1, size_cell)
            table.setItem(row_index, 2, fpath_cell)
            # Increment for the next row
            new_row_index += 1
    
    def on_submit(self):
        project_info = Project()
        experiment_info = Experiment()
        dataset_info = Dataset()
        datafile_info = Datafile()

        project_info.project_name = self.ui.projectNameLineEdit.text()
        project_info.project_id = self.ui.projectIDLineEdit.text()
        project_info.description = self.ui.projectDescriptionLineEdit.toPlainText()
        experiment_info.experiment_name = self.ui.experimentNameLineEdit.text()
        experiment_info.experiment_id = self.ui.experimentIDLineEdit.text()
        experiment_info.project_id = self.ui.projectIDLineEdit.text()
        experiment_info.description = self.ui.experimentDescriptionLineEdit.toPlainText()
        dataset_info.dataset_name = self.ui.datasetNameLineEdit.text()
        dataset_info.dataset_id = self.ui.datasetIDLineEdit.text()
        # Because a dataset can belong to multiple experiments,
        # we are creating a list around the experiment we captured.
        dataset_info.experiment_id = [self.ui.experimentIDLineEdit.text()]

        datafile_info.dataset_id = dataset_info.dataset_id

        table = self.ui.datafiletableWidget
        for row in range(table.rowCount()):
            file_name = table.item(row,0).text()
            size: int = table.item(row,1).data(QtCore.Qt.ItemDataRole.UserRole)
            file_info = FileInfo(name = file_name)
            file_info.size = size
            datafile_info.files.append(file_info)

        self.submitted.emit(project_info, experiment_info, dataset_info, datafile_info)
        self.close()