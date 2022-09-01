from typing import Dict, List
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QWizard, QTableWidget, QTableWidgetItem,QFileDialog, QWizardPage
from ime.ui.ui_add_files_wizard import Ui_ImportDataFiles
from ime.utils import file_size_to_str
from ime.models import Project, Experiment, Dataset, Datafile, FileInfo

class AddFilesWizard(QWizard):

    submitted = QtCore.pyqtSignal(Project, Experiment, Dataset, Datafile)
    page_ids: Dict[str, int] = {}

    def _register_fields(self):
        # Project pages
        proj_page = self.ui.projectPage
        proj_new_page = self.ui.newProjectPage
        proj_existing_page = self.ui.existingProjectPage
        proj_page.registerField("isNewProject", self.ui.newProjectRadioButton)
        proj_page.registerField("isExistingProject", self.ui.existingProjectRadioButton)
        self.ui.newProjectRadioButton.clicked.connect(proj_page.completeChanged)
        self.ui.existingProjectRadioButton.clicked.connect(proj_page.completeChanged)
        proj_existing_page.registerField("existingProject*", self.ui.existingProjectList)
        proj_new_page.registerField("projectIDLineEdit*", self.ui.projectIDLineEdit)
        proj_new_page.registerField("projectNameLineEdit*", self.ui.projectNameLineEdit)
        # Experiment pages
        exp_page = self.ui.experimentPage
        exp_new_page = self.ui.newExperimentPage
        exp_existing_page = self.ui.existingExperimentPage
        exp_page.registerField("isNewExperiment", self.ui.newExperimentRadioButton)
        exp_page.registerField("isExistingExperiment", self.ui.existingExperimentRadioButton)
        self.ui.newExperimentRadioButton.clicked.connect(exp_page.completeChanged)
        self.ui.existingExperimentRadioButton.clicked.connect(exp_page.completeChanged)
        exp_existing_page.registerField("existingExperiment*", self.ui.existingExperimentList)
        exp_new_page.registerField("experimentNameLineEdit*", self.ui.experimentNameLineEdit)
        exp_new_page.registerField("experimentIDLineEdit*", self.ui.experimentIDLineEdit)
        # Dataset pages
        ds_page = self.ui.datasetInfo
        ds_new_page = self.ui.newDatasetPage
        ds_existing_page = self.ui.existingDatasetPage
        ds_page.registerField("isNewDataset", self.ui.newDatasetRadioButton)
        ds_page.registerField("isExistingDataset", self.ui.existingDatasetRadioButton)
        self.ui.newDatasetRadioButton.clicked.connect(ds_page.completeChanged)
        self.ui.existingDatasetRadioButton.clicked.connect(ds_page.completeChanged)
        ds_existing_page.registerField("existingDataset*", self.ui.existingDatasetList)
        ds_new_page.registerField("datasetIDLineEdit*",self.ui.datasetIDLineEdit)
        ds_new_page.registerField("datasetNameLineEdit*",self.ui.datasetNameLineEdit)

    def _make_page_ids(self):
        # Create a dict of page names and their IDs.
        for id in self.pageIds():
            self.page_ids[self.page(id).objectName()] = id

    def nextId(self) -> int:
        current = self.currentId()
        pages = self.page_ids
        if current == pages['newProjectPage']:
            return pages['newExperimentPage']
        elif current == pages['newExperimentPage']:
            return pages['newDatasetPage']
        elif current == pages['newDatasetPage']:
            return pages['includedFilesPage']
        elif current == pages['existingProjectPage']:
            return pages['experimentPage']
        elif current == pages['existingExperimentPage']:
            return pages['datasetPage']
        elif current == pages['existingDatasetPage']:
            return pages['includedFilesPage']
        else:
            return super().nextId()

    def __init__(self):
        super(QWizard, self).__init__()
        self.ui = Ui_ImportDataFiles()
        self.ui.setupUi(self)
        self._make_page_ids()
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

