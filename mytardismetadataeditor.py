import os, sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QToolBar, QAction, QWizard, QTableWidget, QTableWidgetItem, QLineEdit,QWizardPage, QVBoxLayout, QLabel,QFileDialog, QTreeWidget,QTreeWidgetItem
from PyQt5.QtCore import QPersistentModelIndex,QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from isort import file
import yaml
# from mainwindow import Ui_MainWindow
from models import IngestionMetadata, Project, Experiment, Dataset, Datafile, FileInfo
import logging
class MyTardisMetadataEditor(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # load the ui file
        uic.loadUi('MainWindow.ui', self)
        
        self.metadata = IngestionMetadata()

        # define our widgets
        self.actionImport_data_files.triggered.connect(self.openWizardWindow)
        self.actionSave.triggered.connect(self.save_to_yaml)

        self.datasetTreeWidget.itemClicked.connect(self.onClickedDataset)
        self.experimentTreeWidget.itemClicked.connect(self.onClickedExperiment)
        self.projectTreeWidget.itemClicked.connect(self.onClickedProject)

        self.show()

    def onSelectDataset(self, item_id: str):
        # First, look up the dataset value
        dataset_lookup = [
            dataset
            for dataset in self.metadata.datasets
            if dataset.dataset_id == item_id
        ]
        if (len(dataset_lookup) != 1):
            logging.warning("Dataset ID %s could not be found or there are" + 
            "more than one entries.", item_id)
        dataset = dataset_lookup[0]
        # Set controls with value
        self.datasetNameLineEdit.setText(dataset.dataset_name)
        self.datasetIDLineEdit.setText(dataset.dataset_id)
        self.instrumentIDLineEdit.setText(dataset.instrument_id)

    def onSelectDatafile(self, dataset_id: str, file_name: str):
        # First, look up the dataset value
        datafile_lookup = [
            datafile
            for datafile in self.metadata.datafiles
            if datafile.dataset_id == dataset_id
        ]
        if (len(datafile_lookup) != 1):
            logging.warning("Dataset ID %s could not be found or there are" + 
            "more than one entries.", dataset_id)
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
        self.fileInfoFilenameLineEdit.setText(fileinfo.name)


    def onClickedDataset(self):
            item: QTreeWidgetItem = self.datasetTreeWidget.currentItem()
            item_id = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
            props_widget : QStackedWidget = self.datasetTabProps
            if item.parent() is None:
                # This indicates we are looking at a dataset,
                # change stacked widget to show dataset properties
                props_widget.setCurrentIndex(0)
                self.onSelectDataset(item_id)
            else:
                parent = item.parent()
                dataset_id = parent.data(0, QtCore.Qt.ItemDataRole.UserRole)
                props_widget.setCurrentIndex(1)
                self.onSelectDatafile(dataset_id, item_id)


            #self.instrumentIDLineEdit.setText(self.metadata.datasets.instrument_id)

    def onClickedExperiment(self):
            item = self.experimentTreeWidget.currentItem()
            #print("Key=%s,value=%s"%(item.text(0),item.text(1)))
            self.experimentNameLineEdit.setText(item.text(0))
            #print(self.metadata)
            for ds in self.metadata.experiments:
                if ds.experiment_name == item.text(0):
                    self.experimentIDLineEdit.setText(ds.experiment_id)
                    self.experimentDescriptionLineEdit.setText(ds.description)
                else:
                    continue

    def onClickedProject(self):
            item = self.projectTreeWidget.currentItem()
            #print("Key=%s,value=%s"%(item.text(0),item.text(1)))
            self.projectNameLineEdit.setText(item.text(0))
            #print(self.metadata)
            for ds in self.metadata.projects:
                if ds.project_name == item.text(0):
                    self.projectIDLineEdit.setText(ds.project_id)
                    self.projectDescriptionLineEdit.setText(ds.description)
                else:
                    continue

    @QtCore.pyqtSlot(Project,Experiment,Dataset,Datafile)
    def reFresh(self,project_info: Project, experiment_info: Experiment, dataset_info: Dataset, datafile_info: Datafile):
        self.metadata.projects.append(project_info)
        self.metadata.experiments.append(experiment_info)
        self.metadata.datasets.append(dataset_info)
        self.metadata.datafiles.append(datafile_info)

        l1 = QTreeWidgetItem([dataset_info.dataset_name,dataset_info.metadata['Size'],experiment_info.experiment_name])
        l1.setData(0, QtCore.Qt.ItemDataRole.UserRole, dataset_info.dataset_id)

        l2 = QTreeWidgetItem([experiment_info.experiment_name,experiment_info.metadata['Size'],project_info.project_name])
        l2.setData(0, QtCore.Qt.ItemDataRole.UserRole, experiment_info.experiment_id)

        l3 = QTreeWidgetItem([project_info.project_name,project_info.metadata['Size']])
        l3.setData(0, QtCore.Qt.ItemDataRole.UserRole, project_info.project_id)
        

        for file in datafile_info.files:
            file_name = file.name
            file_size = file.metadata['Size']
            l1_child = QTreeWidgetItem([file_name,file_size,""])
            l1_child.setData(0, QtCore.Qt.ItemDataRole.UserRole, file_name)
            l1.addChild(l1_child)
        self.datasetTreeWidget.addTopLevelItem(l1)
        self.experimentTreeWidget.addTopLevelItem(l2)
        self.projectTreeWidget.addTopLevelItem(l3)

    def openWizardWindow(self):  
        self.ui = WindowWizard()
        self.ui.submitted.connect(self.reFresh)
        self.ui.show()
    
    # Save to yaml files
    def save_to_yaml(self):
        filename = QFileDialog.getSaveFileName(self,"Save File",directory = "test.yaml", initialFilter='Yaml File(*.yaml)')[0]
        if filename:
            with open(filename, 'w') as file:
                file.write(self.metadata.to_yaml())

class WindowWizard(QWizard):

    submitted = QtCore.pyqtSignal(Project, Experiment, Dataset, Datafile)

    def __init__(self):
        super(QWizard, self).__init__()
        uic.loadUi('add-files-wizard.ui', self)

        # define out widgets
        self.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        self.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_submit)

    def addFiles_handler(self):
        table = self.datafiletableWidget
        rows = self.open_dialog_box()
        self.addTableRow(table,rows)

    def deleteFiles_handler(self):
        index_list = []
        for model_index in self.datafiletableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.datafiletableWidget.removeRow(index.row())

    def fpath(self):
        return self._fpath

    # calculate sizes of added datafiles in bytes,KB,MB,GB,TB
    def convert_bytes(self,size):
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0

    def open_dialog_box(self):
        filename_mode = QFileDialog()
        filename_mode.setFileMode(QFileDialog.ExistingFiles)
        filename = filename_mode.getOpenFileNames(self, "Open files")  
        fpath = filename[0]
        self._fpath = fpath

        newrows = []
        for f in self._fpath:
            if f !="":
                info = QtCore.QFileInfo(f)
                size = info.size()
                fname = info.fileName()
                size_converted = self.convert_bytes(size)
            newrow = [fname,size_converted, f]
            if newrow not in newrows:
                newrows.append(newrow)
            else:
                continue
        return newrows
    
    def addTableRow(self,table,row_data):
        for lines in row_data:
            row = table.rowCount()
            table.setRowCount(row+1)
            col = 0
            for item in lines:
                cell = QTableWidgetItem(str(item))
                table.setItem(row, col, cell)
                col += 1
    
    def on_submit(self):
        project_info = Project()
        experiment_info = Experiment()
        dataset_info = Dataset()
        datafile_info = Datafile()

        project_info.project_name = self.projectNameLineEdit.text()
        project_info.project_id = self.projectIDLineEdit.text()
        project_info.description = self.projectDescriptionLineEdit.text()
        experiment_info.experiment_name = self.experimentNameLineEdit.text()
        experiment_info.experiment_id = self.experimentIDLineEdit.text()
        experiment_info.project_id = self.projectIDLineEdit.text()
        experiment_info.description = self.experimentdescriptionLineEdit.text()
        dataset_info.dataset_name = self.datasetNameLineEdit.text()
        dataset_info.dataset_id = self.datasetIDLineEdit.text()
        dataset_info.experiment_id = self.experimentIDLineEdit.text()
        datafile_info.dataset_id = dataset_info.dataset_id

        table = self.datafiletableWidget
        ### Calculate the size of dataset, experiment, project - need to modify if "Add data into existing Projects/experiment/datasets" enabled
        B, K, M, G = [], [], [], []
        for row in range(table.rowCount()):
            file_name = table.item(row,0).text()
            size = table.item(row,1).text()
            file_info = FileInfo(name = file_name)
            file_info.metadata['Size'] = size
            datafile_info.files.append(file_info)
            
            l = len(size)
            if size[l-2:] == "bytes":
                B.append(float(size[:l-2]))
            elif size[l-2:] == "KB":
                K.append(float(size[:l-2]))
            elif size[l-2:] == "MB":
                M.append(float(size[:l-2]))
            elif size[l-2:] == "GB":
                G.append(float(size[:l-2]))
        for i in K:
            K[K.index(i)] = i * 1000
        for i in M:
            M[M.index(i)] = i * 1000000
        for i in G: # to convert GigaBytes numbers to KiloBytes
            G[G.index(i)] = i * 1000000000
        size_sum_b = sum(B+K+M+G)
        size_sum = self.convert_bytes(size_sum_b)

        dataset_info.metadata['Size'] = size_sum
        experiment_info.metadata['Size'] = size_sum
        project_info.metadata['Size'] = size_sum

        self.submitted.emit(project_info, experiment_info, dataset_info, datafile_info)
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    window = MyTardisMetadataEditor()
    window.show()
    sys.exit(app.exec_())
