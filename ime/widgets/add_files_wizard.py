from dataclasses import dataclass, field
from typing import Dict, List
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QWizard, QTableWidget, QTableWidgetItem,QFileDialog, QWizardPage
from ime.utils import file_size_to_str
from ime.models import Project, Experiment, Dataset, Datafile
from ime.qt_models import IngestionMetadataModel
from ime.ui.ui_add_files_wizard import Ui_ImportDataFiles
from ime.ui.ui_add_files_wizard_skip import Ui_ImportDataFiles as Ui_ImportDataFiles_skip
#from ime.mytardismetadataeditor import experiment_for_dataset,project_for_experiment
from ime.utils import file_size_to_str


class AddFilesWizardResult:
    """
    A class with the user's choices in the wizard..
    """
    project: Project
    is_new_project: bool
    experiment: Experiment
    is_new_experiment: bool
    dataset: Dataset
    is_new_dataset: bool
    datafile: Datafile

class AddFilesWizard(QWizard):
    """A wizard for adding data files to a metadata model.

    Attributes:
        submitted (QtCore.pyqtSignal): A signal emitted when the wizard is submitted.
        page_ids (Dict[str, int]): A dictionary of page names and their IDs.
        selected_existing_project (Project): The currently selected existing project.
        selected_existing_experiment (Experiment): The currently selected existing experiment.
        selected_existing_dataset (Dataset): The currently selected existing dataset.

    Methods:
        _register_fields(): Set up the fields and connect signals for isComplete states.
        _make_page_ids(): Create a dictionary of page names and their IDs.
        nextId() -> int: Determine which page the wizard should advance to.
        __init__(metadataModel: IngestionMetadataModel): Initialize the wizard with the given metadata model.
        addFiles_handler(): Handle adding files to the table.
        deleteFiles_handler(): Handle deleting files from the table.
    """
    submitted = QtCore.pyqtSignal(AddFilesWizardResult)
    page_ids: Dict[str, int] = {}
    selected_existing_project: Project
    selected_existing_experiment: Experiment
    selected_existing_dataset: Dataset

    def _register_fields(self):
        """Set up the fields and connect signals for isComplete states."""
        # Project pages
        proj_page = self.ui.projectPage
        proj_new_page = self.ui.newProjectPage
        proj_page.registerField("isNewProject", self.ui.newProjectRadioButton)
        proj_page.registerField("isExistingProject", self.ui.existingProjectRadioButton)
        self.ui.newProjectRadioButton.clicked.connect(proj_page.completeChanged)
        self.ui.existingProjectRadioButton.clicked.connect(proj_page.completeChanged)
        self.ui.existingProjectList.currentIndexChanged.connect(proj_page.completeChanged)
        proj_page.registerField("existingProject", self.ui.existingProjectList)
        proj_new_page.registerField("projectIDLineEdit*", self.ui.projectIDLineEdit)
        proj_new_page.registerField("projectNameLineEdit*", self.ui.projectNameLineEdit)
        # Experiment pages
        exp_page = self.ui.experimentPage
        exp_new_page = self.ui.newExperimentPage
        exp_page.registerField("isNewExperiment", self.ui.newExperimentRadioButton)
        exp_page.registerField("isExistingExperiment", self.ui.existingExperimentRadioButton)
        self.ui.newExperimentRadioButton.clicked.connect(exp_page.completeChanged)
        self.ui.existingExperimentRadioButton.clicked.connect(exp_page.completeChanged)
        self.ui.existingExperimentList.currentIndexChanged.connect(exp_page.completeChanged)
        exp_page.registerField("existingExperiment", self.ui.existingExperimentList)
        exp_new_page.registerField("experimentNameLineEdit*", self.ui.experimentNameLineEdit)
        exp_new_page.registerField("experimentIDLineEdit*", self.ui.experimentIDLineEdit)
        # Dataset pages
        ds_page = self.ui.datasetPage
        ds_new_page = self.ui.newDatasetPage
        ds_page.registerField("isNewDataset", self.ui.newDatasetRadioButton)
        ds_page.registerField("isExistingDataset", self.ui.existingDatasetRadioButton)
        self.ui.newDatasetRadioButton.clicked.connect(ds_page.completeChanged)
        self.ui.existingDatasetRadioButton.clicked.connect(ds_page.completeChanged)
        self.ui.existingDatasetList.currentIndexChanged.connect(ds_page.completeChanged)
        ds_page.registerField("existingDataset", self.ui.existingDatasetList)
        ds_new_page.registerField("datasetIDLineEdit*",self.ui.datasetIDLineEdit)
        ds_new_page.registerField("datasetNameLineEdit*",self.ui.datasetNameLineEdit)

    def _make_page_ids(self):
        """
        Creates a dictionary of page names and their corresponding IDs. The page IDs are obtained by calling the 
        `pageIds()` method of the QWizard, and the objectName() of each page is used as the key in the dictionary.
        """
        for id in self.pageIds():
            self.page_ids[self.page(id).objectName()] = id

    def nextId(self) -> int:
        # Function for determining which page the wizard should advance to.
        # Custom WizardPages in add_files_wizard_pages have their own nextId()
        # logic and they are used in the else clause, which calls the default
        # nextId function.
        """
        Determines which page the wizard should advance to based on the user's input. The function checks the current 
        page ID against the page IDs in the `self.page_ids` dictionary, and returns the next page ID based on the 
        user's input. If a custom WizardPage has its own `nextId()` function, it is called instead of the default 
        `nextId()` function. The following is the logic for determining the next page ID:
    
        - If the current page is the 'introductionPage':
            - If there are existing projects, go to the 'projectPage', else go to the 'newProjectPage'.
        - If the current page is the 'newProjectPage', go to the 'newExperimentPage'.
        - If the current page is the 'newExperimentPage', go to the 'newDatasetPage'.
        - If the current page is the 'newDatasetPage', go to the 'includedFilesPage'.
        - Otherwise, call the default `nextId()` function.
        """
        current = self.currentId()
        pages = self.page_ids
        if current == pages['introductionPage']:
            # Check if there are existing projects.
            # If there are, go to the choice page, otherwise go to the new project page.
            if self.metadataModel.projects.rowCount() > 0:
                return pages['projectPage']
            else:
                # Need to set the fields manually since we're not showing
                # user the project choice page. Ditto for the fields
                # in experiment and dataset pages. 
                self.setField('isNewProject', True)
                self.setField('isExistingProject', False)
                return pages['newProjectPage']
        if current == pages['newProjectPage']:
            self.setField('isNewExperiment', True)
            self.setField('isExistingExperiment', False)
            return pages['newExperimentPage']
        elif current == pages['newExperimentPage']:
            self.setField('isNewDataset', True)
            self.setField('isExistingDataset', False)
            return pages['newDatasetPage']
        elif current == pages['newDatasetPage']:
            return pages['includedFilesPage']
        else:
            return super().nextId()

    def __init__(self, metadataModel: IngestionMetadataModel):
        """
        Initializes the QWizard with the specified `metadataModel`. The UI is set up using the `Ui_ImportDataFiles`
        class. The page IDs are created using the `_make_page_ids()` method and the fields are registered using 
        the `_register_fields()` method. The `datafileAddPushButton` and `datafileDeletePushButton` buttons are 
        connected to their corresponding handler methods.
        """
        super(QWizard, self).__init__()
        self.ui = Ui_ImportDataFiles()
        self.metadataModel = metadataModel
        self.ui.setupUi(self)
        self._make_page_ids()
        self._register_fields()
        # define out widgets
        self.ui.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        self.ui.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_submit)

    def addFiles_handler(self):
        """Add files to the table.

        Gets the table, calls the open_add_files_dialog() method to open a file dialog and get the list of files to add.
        Passes the table and the list of files to add to the add_file_table_rows() method.

        Returns:
            None.
        """
        table = self.ui.datafiletableWidget
        files_to_add = self.open_add_files_dialog()
        self.add_file_table_rows(table,files_to_add)

    def deleteFiles_handler(self):
        """Delete files from the table.

        Gets the selected rows from the table, creates a list of QModelIndex objects for those rows.
        Passes each QModelIndex object to removeRow() method to delete that row from the table.

        Returns:
            None.
        """
        index_list = []
        for model_index in self.ui.datafiletableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.ui.datafiletableWidget.removeRow(index.row())

    # calculate sizes of added datafiles in bytes,KB,MB,GB,TB

    def open_add_files_dialog(self) -> List[QtCore.QFileInfo]:
        """Open a file dialog and get the list of files to add.

        Creates a file dialog, opens it to allow the user to select files to add.
        Returns the list of QFileInfo objects for the selected files.

        Returns:
            A list of QFileInfo objects for the selected files.
        """

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
        """Add rows to the table.

        Gets the table and the list of files to add.
        Iterates over the list of files to add and creates a row in the table for each file.
        Sets the filename, size, and file path as items in the row.

        Args:
            table: A QTableWidget object to add rows to.
            files_to_add: A list of QFileInfo objects to create rows for.

        Returns:
            None.
        """
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
        """
        Builds a result class based on the user's choices and emits them through the signal.

        Returns:
            None

        """
        result = AddFilesWizardResult()
        result.is_new_project = self.field('isNewProject')
        result.is_new_experiment = self.field('isNewExperiment')
        result.is_new_dataset = self.field('isNewDataset')
        if self.field('isExistingProject'):
            result.project = self.selected_existing_project
        else:
            result.project = Project()
            result.project.project_name = self.ui.projectNameLineEdit.text()
            result.project.project_id = self.ui.projectIDLineEdit.text()
            result.project.description = self.ui.projectDescriptionLineEdit.toPlainText()
            
        if self.field('isExistingExperiment'):
            result.experiment = self.selected_existing_experiment
        else:
            result.experiment = Experiment()
            result.experiment.experiment_name = self.ui.experimentNameLineEdit.text()
            result.experiment.experiment_id = self.ui.experimentIDLineEdit.text()
            result.experiment.project_id = result.project.project_id
            result.experiment.description = self.ui.experimentDescriptionLineEdit.toPlainText()

        if self.field('isExistingDataset'):
            result.dataset = self.selected_existing_dataset
        else:
            result.dataset = Dataset()
            result.dataset.dataset_name = self.ui.datasetNameLineEdit.text()
            result.dataset.dataset_id = self.ui.datasetIDLineEdit.text()
            # Because a dataset can belong to multiple experiments,
            # we are creating a list around the experiment we captured.
            result.dataset.experiment_id = [result.experiment.experiment_id]
        result.datafile = Datafile()
        result.datafile.dataset_id = result.dataset.dataset_id

        table = self.ui.datafiletableWidget
        for row in range(table.rowCount()):
            file_name = table.item(row,0).text()
            size: int = table.item(row,1).data(QtCore.Qt.ItemDataRole.UserRole)
            result.datafile.filename=file_name
            result.datafile.size=size

        self.submitted.emit(result)

class AddFilesWizardSkipDataset(QWizard):
    """A wizard for adding data files to a metadata model.

    Attributes:
        submitted (QtCore.pyqtSignal): A signal emitted when the wizard is submitted.
        page_ids (Dict[str, int]): A dictionary of page names and their IDs.
        selected_existing_project (Project): The currently selected existing project.
        selected_existing_experiment (Experiment): The currently selected existing experiment.
        selected_existing_dataset (Dataset): The currently selected existing dataset.

    Methods:
        _register_fields(): Set up the fields and connect signals for isComplete states.
        _make_page_ids(): Create a dictionary of page names and their IDs.
        nextId() -> int: Determine which page the wizard should advance to.
        __init__(metadataModel: IngestionMetadataModel): Initialize the wizard with the given metadata model.
        addFiles_handler(): Handle adding files to the table.
        deleteFiles_handler(): Handle deleting files from the table.
    """
    submitted = QtCore.pyqtSignal(AddFilesWizardResult)
    page_ids: Dict[str, int] = {}
    selected_existing_project: Project
    selected_existing_experiment: Experiment
    selected_existing_dataset: Dataset

    def _register_fields(self):
        # Set up the fields and connect signals for isComplete states.
        # dataset pages
        ds_page = self.ui.pedPage
        ds_new_page = self.ui.newDatasetPage

        self.ui.existingProjectList_3.currentIndexChanged.connect(ds_page.completeChanged)
        self.ui.existingExperimentList_2.currentIndexChanged.connect(ds_page.completeChanged)
        self.ui.existingDatasetList_1.currentIndexChanged.connect(ds_page.completeChanged)

        ds_page.registerField("isExistingProject", self.ui.existingProjectList_3)
        ds_page.registerField("isExistingExperiment", self.ui.existingExperimentList_2)
        ds_page.registerField("isExistingDataset", self.ui.existingDatasetList_1)

        ds_new_page.registerField("datasetIDLineEdit*",self.ui.datasetIDLineEdit)
        ds_new_page.registerField("datasetNameLineEdit*",self.ui.datasetNameLineEdit)

    def _make_page_ids(self):
        """
        Creates a dictionary of page names and their corresponding IDs. The page IDs are obtained by calling the 
        `pageIds()` method of the QWizard, and the objectName() of each page is used as the key in the dictionary.
        """
        for id in self.pageIds():
            self.page_ids[self.page(id).objectName()] = id

    def __init__(self, metadataModel: IngestionMetadataModel, ds_data: Datafile, exp_data: Experiment, pro_data: Project):
        """
        Initializes the QWizard with the specified `metadataModel`. The UI is set up using the `Ui_ImportDataFiles`
        class. The page IDs are created using the `_make_page_ids()` method and the fields are registered using 
        the `_register_fields()` method. The `datafileAddPushButton` and `datafileDeletePushButton` buttons are 
        connected to their corresponding handler methods.
        """
        super(QWizard, self).__init__()
        self.ui = Ui_ImportDataFiles_skip()
        self.metadataModel = metadataModel
        self.ui.setupUi(self)
        self._make_page_ids()
        self._register_fields()
        pages = self.page_ids
        self.setStartId(pages['pedPage'])
        #exp_name = self.experiment_for_dataset(item_data.dataset_name)
        #proj_name = self.project_for_experiment(exp_name)
        # customise the pedPage, pePage, and pPage with item_data
        #print(ds_data, exp_data, pro_data)
        #self.ui.existingDatasetList_1 = ds_data.dataset_name
        #self.ui.existingExperimentList_2 = exp_data.experiment_name
        #self.ui.existingProjectList_3 = pro_data.project_name

        # define out widgets
        self.ui.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        self.ui.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_submit)

    def addFiles_handler(self):
        """Add files to the table.

        Gets the table, calls the open_add_files_dialog() method to open a file dialog and get the list of files to add.
        Passes the table and the list of files to add to the add_file_table_rows() method.

        Returns:
            None.
        """
        table = self.ui.datafiletableWidget
        files_to_add = self.open_add_files_dialog()
        self.add_file_table_rows(table,files_to_add)

    def deleteFiles_handler(self):
        """Delete files from the table.

        Gets the selected rows from the table, creates a list of QModelIndex objects for those rows.
        Passes each QModelIndex object to removeRow() method to delete that row from the table.

        Returns:
            None.
        """
        index_list = []
        for model_index in self.ui.datafiletableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.ui.datafiletableWidget.removeRow(index.row())

    # calculate sizes of added datafiles in bytes,KB,MB,GB,TB

    def open_add_files_dialog(self) -> List[QtCore.QFileInfo]:
        """Open a file dialog and get the list of files to add.

        Creates a file dialog, opens it to allow the user to select files to add.
        Returns the list of QFileInfo objects for the selected files.

        Returns:
            A list of QFileInfo objects for the selected files.
        """
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
        """Add rows to the table.

        Gets the table and the list of files to add.
        Iterates over the list of files to add and creates a row in the table for each file.
        Sets the filename, size, and file path as items in the row.

        Args:
            table: A QTableWidget object to add rows to.
            files_to_add: A list of QFileInfo objects to create rows for.

        Returns:
            None.
        """
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
        """
        Builds a result class based on the user's choices and emits them through the signal.

        Returns:
            None

        """
        result = AddFilesWizardResult()
        result.is_new_project = self.field('isNewProject')
        result.is_new_experiment = self.field('isNewExperiment')
        result.is_new_dataset = self.field('isNewDataset')

        result.project = self.selected_existing_project
        result.experiment = self.selected_existing_experiment
        result.dataset = self.selected_existing_dataset

        result.datafile = Datafile()
        result.datafile.dataset_id = result.dataset.dataset_id

        ### Create new Datafile object and append to result.datafile.files
        
        table = self.ui.datafiletableWidget
        for row in range(table.rowCount()):
            file_name = table.item(row,0).text()
            size: int = table.item(row,1).data(QtCore.Qt.ItemDataRole.UserRole)
            result.datafile.filename=file_name
            result.datafile.size=size
        #print(result.dataset)
        self.submitted.emit(result)
        self.close()

class AddFilesWizardSkipExperiment(QWizard):
    submitted = QtCore.pyqtSignal(AddFilesWizardResult)
    page_ids: Dict[str, int] = {}
    selected_existing_project: Project
    selected_existing_experiment: Experiment
    selected_existing_dataset: Dataset

    def _register_fields(self):
        # Experiment pages
        exp_page = self.ui.pePage
        exp_new_page = self.ui.newExperimentPage

        self.ui.existingProjectList_2.currentIndexChanged.connect(exp_page.completeChanged)
        exp_page.registerField("isExistingProject", self.ui.existingProjectList_2)

        self.ui.existingExperimentList_1.currentIndexChanged.connect(exp_page.completeChanged)
        exp_page.registerField("isExistingExperiment", self.ui.existingExperimentList_1)
        exp_new_page.registerField("experimentNameLineEdit*", self.ui.experimentNameLineEdit)
        exp_new_page.registerField("experimentIDLineEdit*", self.ui.experimentIDLineEdit)
        
        # Dataset pages
        ds_new_page = self.ui.newDatasetPage
        # temporary!!!!!!!
        #exp_page.registerField("isNewDataset", self.ui.existingProjectList_2)
        ds_new_page.registerField('isNewDataset',self.ui.datasetNameLabel_2)
        ds_new_page.registerField("datasetIDLineEdit*",self.ui.datasetIDLineEdit)
        ds_new_page.registerField("datasetNameLineEdit*",self.ui.datasetNameLineEdit)

    def _make_page_ids(self):
        """
        Creates a dictionary of page names and their corresponding IDs. The page IDs are obtained by calling the 
        `pageIds()` method of the QWizard, and the objectName() of each page is used as the key in the dictionary.
        """
        for id in self.pageIds():
            self.page_ids[self.page(id).objectName()] = id

    def nextId(self) -> int:
        # Function for determining which page the wizard should advance to.
        # Custom WizardPages in add_files_wizard_pages have their own nextId()
        # logic and they are used in the else clause, which calls the default
        # nextId function.
        current = self.currentId()
        pages = self.page_ids

        if current == pages['pePage']:
            self.setField('isNewProject', False)
            self.setField('isNewExperiment', False)
            self.setField('isNewDataset', True)
            return pages['newDatasetPage']
        elif current == pages['newDatasetPage']:
            return pages['includedFilesPage']
        else:
            return super().nextId()

    def __init__(self, metadataModel: IngestionMetadataModel):
        """
        Initializes the QWizard with the specified `metadataModel`. The UI is set up using the `Ui_ImportDataFiles`
        class. The page IDs are created using the `_make_page_ids()` method and the fields are registered using 
        the `_register_fields()` method. The `datafileAddPushButton` and `datafileDeletePushButton` buttons are 
        connected to their corresponding handler methods.
        """
        super(QWizard, self).__init__()
        self.ui = Ui_ImportDataFiles_skip()
        self.metadataModel = metadataModel
        self.ui.setupUi(self)
        self._make_page_ids()
        self._register_fields()
        pages = self.page_ids
        self.setStartId(pages['pePage'])
        # define out widgets
        self.ui.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        self.ui.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_submit)

    def addFiles_handler(self):
        """Add files to the table.

        Gets the table, calls the open_add_files_dialog() method to open a file dialog and get the list of files to add.
        Passes the table and the list of files to add to the add_file_table_rows() method.

        Returns:
            None.
        """
        table = self.ui.datafiletableWidget
        files_to_add = self.open_add_files_dialog()
        self.add_file_table_rows(table,files_to_add)

    def deleteFiles_handler(self):
        """Delete files from the table.

        Gets the selected rows from the table, creates a list of QModelIndex objects for those rows.
        Passes each QModelIndex object to removeRow() method to delete that row from the table.

        Returns:
            None.
        """
        index_list = []
        for model_index in self.ui.datafiletableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.ui.datafiletableWidget.removeRow(index.row())

    # calculate sizes of added datafiles in bytes,KB,MB,GB,TB
    def open_add_files_dialog(self) -> List[QtCore.QFileInfo]:
        """Open a file dialog and get the list of files to add.

        Creates a file dialog, opens it to allow the user to select files to add.
        Returns the list of QFileInfo objects for the selected files.

        Returns:
            A list of QFileInfo objects for the selected files.
        """
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
        """Add rows to the table.

        Gets the table and the list of files to add.
        Iterates over the list of files to add and creates a row in the table for each file.
        Sets the filename, size, and file path as items in the row.

        Args:
            table: A QTableWidget object to add rows to.
            files_to_add: A list of QFileInfo objects to create rows for.

        Returns:
            None.
        """
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
        """
        Builds a result class based on the user's choices and emits them through the signal.

        Returns:
            None

        """
        result = AddFilesWizardResult()
        result.is_new_project = self.field('isNewProject')
        result.is_new_experiment = self.field('isNewExperiment')
        result.is_new_dataset = self.field('isNewDataset')

        result.project = self.selected_existing_project
        result.experiment = self.selected_existing_experiment
        #print(result.project,result.experiment)

        ### assume new dataset
        result.dataset = Dataset()
        result.dataset.dataset_name = self.ui.datasetNameLineEdit.text()
        result.dataset.dataset_id = self.ui.datasetIDLineEdit.text()
        # Because a dataset can belong to multiple experiments,
        # we are creating a list around the experiment we captured.
        result.dataset.experiment_id = [result.experiment.experiment_id]

        result.datafile = Datafile()
        result.datafile.dataset_id = result.dataset.dataset_id
        #print(result.dataset,result.datafile)

        table = self.ui.datafiletableWidget
        for row in range(table.rowCount()):
            file_name = table.item(row,0).text()
            size: int = table.item(row,1).data(QtCore.Qt.ItemDataRole.UserRole)
            result.datafile.filename=file_name
            result.datafile.size=size
        #print(result.experiment,result.project)
        self.submitted.emit(result)
        self.close()

class AddFilesWizardSkipProject(QWizard):
    """
    A wizard for adding new files to an existing project, skipping the project selection page.

    Signals:
    submitted: A PyQt signal emitted when the wizard is submitted.

    Attributes:
    page_ids (Dict[str, int]): A dictionary containing the object names of each page in the wizard as keys, and their
                               corresponding IDs as values.
    selected_existing_project (Project): The currently selected existing project.
    selected_existing_experiment (Experiment): The currently selected existing experiment.
    selected_existing_dataset (Dataset): The currently selected existing dataset.
    """
    submitted = QtCore.pyqtSignal(AddFilesWizardResult)
    page_ids: Dict[str, int] = {}
    selected_existing_project: Project
    selected_existing_experiment: Experiment
    selected_existing_dataset: Dataset

    def _register_fields(self):
        # Set up the fields and connect signals for isComplete states.
        """
        Register fields for each page in the wizard.

        This method sets up the fields and connects signals for the isComplete states of each page.

        Returns:
        None.
        """
        # Experiment pages
        pro_page = self.ui.pPage
        #ds_new_page = self.ui.newDatasetPage

        self.ui.existingProjectList_1.currentIndexChanged.connect(pro_page.completeChanged)
        pro_page.registerField("isExistingProject", self.ui.existingProjectList_1)

        exp_new_page = self.ui.newExperimentPage
        ds_new_page = self.ui.newDatasetPage
        
        pro_page.registerField("isNewExperiment", self.ui.existingProjectList_1)
        
        #exp_new_page.registerField(isNew)
        exp_new_page.registerField('experimentNameLineEdit*',self.ui.experimentNameLineEdit)
        exp_new_page.registerField('experimentIDLineEdit*',self.ui.experimentIDLineEdit)
        ds_new_page.registerField("datasetIDLineEdit*",self.ui.datasetIDLineEdit)
        ds_new_page.registerField("datasetNameLineEdit*",self.ui.datasetNameLineEdit)
        ds_new_page.registerField('isNewDataset',self.ui.datasetNameLabel_2)

    def _make_page_ids(self):
        """
        Create a dictionary of page names and their corresponding IDs.

        This method creates a dictionary of page names and their corresponding IDs. The page IDs are obtained by calling
        the `pageIds()` method of the QWizard, and the objectName() of each page is used as the key in the dictionary.

        Returns:
        None.
        """
        for id in self.pageIds():
            self.page_ids[self.page(id).objectName()] = id
    
    def nextId(self) -> int:
        # Function for determining which page the wizard should advance to.
        # Custom WizardPages in add_files_wizard_pages have their own nextId()
        # logic and they are used in the else clause, which calls the default
        # nextId function.
        """
        Determine which page the wizard should advance to.

        This method determines which page the wizard should advance to based on the current page. Custom WizardPages in
        add_files_wizard_pages have their own nextId() logic and they are used in the else clause, which calls the
        default nextId function.

        Returns:
        The ID of the next page in the wizard.
        """
        current = self.currentId()
        pages = self.page_ids

        if current == pages['pPage']:
            self.setField('isNewProject', False)
            self.setField('isNewExperiment', True)
            self.setField('isNewDataset', True)
            return pages['newExperimentPage']
        elif current == pages['newExperimentPage']:
            return pages['newDatasetPage']
        elif current == pages['newDatasetPage']:
            return pages['includedFilesPage']
        else:
            return super().nextId()
 
    def __init__(self, metadataModel: IngestionMetadataModel):
        """
        Initializes the QWizard with the specified `metadataModel`. The UI is set up using the `Ui_ImportDataFiles`
        class. The page IDs are created using the `_make_page_ids()` method and the fields are registered using 
        the `_register_fields()` method. The `datafileAddPushButton` and `datafileDeletePushButton` buttons are 
        connected to their corresponding handler methods.
        """
        super(QWizard, self).__init__()
        self.ui = Ui_ImportDataFiles_skip()
        self.metadataModel = metadataModel
        self.ui.setupUi(self)
        self._make_page_ids()
        self._register_fields()
        pages = self.page_ids 
        self.setStartId(pages['pPage'])
        # define out widgets
        self.ui.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        self.ui.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_submit)

    def addFiles_handler(self):
        """Add files to the table.

        Gets the table, calls the open_add_files_dialog() method to open a file dialog and get the list of files to add.
        Passes the table and the list of files to add to the add_file_table_rows() method.

        Returns:
            None.
        """
        table = self.ui.datafiletableWidget
        files_to_add = self.open_add_files_dialog()
        self.add_file_table_rows(table,files_to_add)

    def deleteFiles_handler(self):
        """Delete files from the table.

        Gets the selected rows from the table, creates a list of QModelIndex objects for those rows.
        Passes each QModelIndex object to removeRow() method to delete that row from the table.

        Returns:
            None.
        """
        index_list = []
        for model_index in self.ui.datafiletableWidget.selectionModel().selectedRows():
            index = QtCore.QPersistentModelIndex(model_index)
            index_list.append(index)
        for index in index_list:
            self.ui.datafiletableWidget.removeRow(index.row())

    # calculate sizes of added datafiles in bytes,KB,MB,GB,TB

    def open_add_files_dialog(self) -> List[QtCore.QFileInfo]:
        """Open a file dialog and get the list of files to add.

        Creates a file dialog, opens it to allow the user to select files to add.
        Returns the list of QFileInfo objects for the selected files.

        Returns:
            A list of QFileInfo objects for the selected files.
        """
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
        """Add rows to the table.

        Gets the table and the list of files to add.
        Iterates over the list of files to add and creates a row in the table for each file.
        Sets the filename, size, and file path as items in the row.

        Args:
            table: A QTableWidget object to add rows to.
            files_to_add: A list of QFileInfo objects to create rows for.

        Returns:
            None.
        """
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
        """
        Builds a result class based on the user's choices and emits them through the signal.

        Returns:
            None

        """
        result = AddFilesWizardResult()
        result.is_new_project = self.field('isNewProject')
        result.is_new_experiment = self.field('isNewExperiment')
        result.is_new_dataset = self.field('isNewDataset')
        result.project = self.selected_existing_project

        ### assume new experiment
        result.experiment = Experiment()
        result.experiment.title = self.ui.experimentNameLineEdit.text()
        result.experiment.experiment_id = self.ui.experimentIDLineEdit.text()
        result.experiment.project_id = result.project.project_id
        result.experiment.description = self.ui.experimentDescriptionLineEdit.toPlainText()
        ### assume new dataset
        result.dataset = Dataset()
        result.dataset.dataset_name = self.ui.datasetNameLineEdit.text()
        result.dataset.dataset_id = self.ui.datasetIDLineEdit.text()
        # Because a dataset can belong to multiple experiments,
        # we are creating a list around the experiment we captured.
        result.dataset.experiment_id = [result.experiment.experiment_id]

        result.datafile = Datafile()
        result.datafile.dataset_id = result.dataset.dataset_id

        table = self.ui.datafiletableWidget
        for row in range(table.rowCount()):
            file_name = table.item(row,0).text()
            size: int = table.item(row,1).data(QtCore.Qt.ItemDataRole.UserRole)
            result.datafile.filename=file_name
            result.datafile.size=size
        #print(result.dataset,result.experiment,result.project)
        self.submitted.emit(result)
        self.close()