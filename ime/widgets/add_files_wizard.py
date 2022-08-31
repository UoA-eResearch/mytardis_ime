from typing import List
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QWizard, QTableWidget, QTableWidgetItem,QFileDialog, QWizardPage
from ime.ui.ui_add_files_wizard import Ui_ImportDataFiles
from ime.utils import file_size_to_str
from ime.models import Project, Experiment, Dataset, Datafile, FileInfo

class AddFilesWizard(QWizard):

    submitted = QtCore.pyqtSignal(Project, Experiment, Dataset, Datafile)

    def _register_fields(self):
        proj_page = self.ui.wizardPage1
        proj_page.registerField("isNewProject", self.ui.newProjectRadioButton)
        proj_page.registerField("isExistingProject", self.ui.existingProjectRadioButton)
        proj_page.registerField("existingProject", self.ui.existingProjectComboBox)
        proj_page.registerField("projectIDLineEdit", self.ui.projectIDLineEdit)
        proj_page.registerField("projectNameLineEdit", self.ui.projectNameLineEdit)
        self.ui.projectIDLineEdit.textChanged.connect(proj_page.completeChanged)
        
        self.ui.existingProjectRadioButton.toggled.connect(lambda checked: self.ui.existingProjectForm.setVisible(checked))
        self.ui.newProjectRadioButton.toggled.connect(lambda checked: self.ui.newProjectForm.setVisible(checked))
        exp_page = self.ui.wizardPage2
        exp_page.registerField("isNewExperiment", self.ui.newExperimentRadioButton)
        exp_page.registerField("isExistingExperiment", self.ui.existingExperimentRadioButton)
        exp_page.registerField("existingExperiment", self.ui.existingDatasetComboBox)
        exp_page.registerField("experimentNameLineEdit", self.ui.experimentNameLineEdit)
        exp_page.registerField("experimentIDLineEdit", self.ui.experimentIDLineEdit)
        self.ui.existingExperimentRadioButton.toggled.connect(lambda checked: self.ui.existingExperimentForm.setVisible(checked))
        self.ui.newExperimentRadioButton.toggled.connect(lambda checked: self.ui.newExperimentForm.setVisible(checked))
        ds_page = self.ui.datasetInfo
        ds_page.registerField("isNewDataset", self.ui.newDatasetRadioButton)
        ds_page.registerField("isExistingDataset", self.ui.existingDatasetRadioButton)
        ds_page.registerField("existingDataset", self.ui.existingDatasetComboBox)
        ds_page.registerField("datasetIDLineEdit",self.ui.datasetIDLineEdit)
        ds_page.registerField("datasetNameLineEdit",self.ui.datasetNameLineEdit)
        self.ui.existingDatasetRadioButton.toggled.connect(lambda checked: self.ui.existingDatasetForm.setVisible(checked))
        self.ui.newDatasetRadioButton.toggled.connect(lambda checked: self.ui.newDatasetForm.setVisible(checked))

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

