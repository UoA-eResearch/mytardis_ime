from typing import Dict, List, Optional
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QLineEdit,  QWizard
from ime.models import Project, Experiment, Dataset, Datafile
from ime.qt_models import IngestionMetadataModel
from ime.ui.ui_add_files_wizard import Ui_ImportDataFiles
from pathlib import Path
from ime.parser.image_parser import ImageProcessor

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
    #datafile: Datafile 
    file_list: List[Datafile]

class UniqueValueValidator(QValidator):
    """A Validator for Qt Line Edits to ensure the user input
    value is unique in a list.    """
    def __init__(self, existing_values_list: list[str], parent: QtCore.QObject | None = None) -> None:
        self.existing = set(existing_values_list)
        super().__init__(parent)

    def validate(self, to_validate: str, a1: int) -> tuple[QValidator.State, str, int]:
        """Override method to validate that a value is unique.

        Args:
            to_validate (str): The value to validate.
            a1 (int): Cursor position

        Returns:
            tuple[QValidator.State, str, int]: A tuple with whether the input is acceptable,
            a new suggested value and new cursor position.
        """
        if to_validate in self.existing:
            return tuple([QValidator.State.Intermediate, to_validate, a1]) # type: ignore
        return tuple([QValidator.State.Acceptable, to_validate, a1]) # type: ignore

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

    def _set_start_id(self) -> None:
        """Sets the starting wizard page.
        """
        if self.selected_existing_dataset is not None:
            # If a dataset is passed in, then start with add to dataset page.
            self.setStartId(self.page_ids['skipDatasetPage'])
        elif self.selected_existing_experiment is not None:
            # If an experiment is passed in, then start with add to experiment page.
            self.setStartId(self.page_ids['skipExpPage'])
        elif self.selected_existing_project is not None:
            # If a project is passed in, then start with add to project page.
            self.setStartId(self.page_ids['skipProjectPage'])
        else:
            # If nothing is passed in, then start with the introduction page.
            if not self.metadataModel.metadata.is_empty():
            # If there is already metadata, skip the introduction
            # page.
                self.setStartId(self.page_ids['projectPage'])
            else:
                self.setStartId(self.page_ids['introductionPage'])


    def _set_existing_status(self) -> None:
        """Private method for initialising the existing fields in constructor.
        In cases where a project, experiment or dataset are passed in. 
        """
        if self.selected_existing_project is not None:
            self.setField('isExistingProject', True)
        if self.selected_existing_experiment is not None:
            self.setField('isExistingExperiment', True)
        if self.selected_existing_dataset is not None:
            self.setField('isExistingDataset', True)
        

    def __init__(self, 
            metadataModel: IngestionMetadataModel, 
            selected_project: Optional[Project] = None,
            selected_experiment: Optional[Experiment] = None,
            selected_dataset: Optional[Dataset] = None
        ):
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
        self.selected_existing_project = selected_project
        self.selected_existing_experiment = selected_experiment
        self.selected_existing_dataset = selected_dataset
        self._set_existing_status()
        self._set_start_id()
        # define out widgets
        # self.ui.datafileAddPushButton.clicked.connect(self.addFiles_handler)
        # self.ui.dirAddPushButton.clicked.connect(self.addDir_handler)
        # self.ui.datafileDeletePushButton.clicked.connect(self.deleteFiles_handler)
        self.button(QtWidgets.QWizard.FinishButton).clicked.connect(self.on_submit)
        self._setup_validated_input()


    def _update_widget_validation_style(self,line_edit: QLineEdit):
        """Private method that gets called to update line edit style
        to reflect validation status.

        Args:
            line_edit (QLineEdit): The line edit to update.
        """
        if line_edit.hasAcceptableInput():
            line_edit.setStyleSheet("")
        else:
            # Add pink to indicate invalid input.
            line_edit.setStyleSheet("QLineEdit { background-color: pink; }")

    def _setup_validated_input(self):
        """Private method to set up uniqueness validation for
        Project/Experiment/Dataset ID entries.
        """
        # Projects
        all_project_ids: list[str] = []
        for project in self.metadataModel.metadata.projects:
            all_project_ids += project.identifiers or []
        new_id_validator = UniqueValueValidator(all_project_ids, self)
        proj_line_edit = self.ui.projectIDLineEdit
        proj_line_edit.setValidator(new_id_validator)
        proj_line_edit.textEdited.connect(lambda: self._update_widget_validation_style(proj_line_edit))
        # Experiments
        all_exp_ids: list[str] = []
        for exp in self.metadataModel.metadata.experiments:
            all_exp_ids += exp.identifiers or []
        new_id_validator = UniqueValueValidator(all_exp_ids, self)
        exp_line_edit = self.ui.experimentIDLineEdit
        exp_line_edit.setValidator(new_id_validator)
        exp_line_edit.textEdited.connect(lambda: self._update_widget_validation_style(exp_line_edit))
        # Datasets
        all_dataset_ids: list[str] = []
        for ds in self.metadataModel.metadata.datasets:
            all_dataset_ids += ds.identifiers or []
        new_id_validator = UniqueValueValidator(all_dataset_ids, self)
        ds_line_edit = self.ui.datasetIDLineEdit
        ds_line_edit.setValidator(new_id_validator)
        ds_line_edit.textEdited.connect(lambda: self._update_widget_validation_style(ds_line_edit))
    
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
            assert self.selected_existing_project is not None
            result.project = self.selected_existing_project
        else:
            result.project = Project()
            result.project._store = self.metadataModel.metadata
            result.project.name = self.ui.projectNameLineEdit.text()
            result.project.identifiers_delegate.add(self.ui.projectIDLineEdit.text())
            result.project.description = self.ui.projectDescriptionLineEdit.toPlainText()
            
        if self.field('isExistingExperiment'):
            assert self.selected_existing_experiment is not None
            result.experiment = self.selected_existing_experiment
        else:
            result.experiment = Experiment()
            result.experiment._store = self.metadataModel.metadata
            result.experiment.title = self.ui.experimentNameLineEdit.text()
            result.experiment.identifiers_delegate.add(self.ui.experimentIDLineEdit.text())
            result.experiment.project_id = result.project.identifiers_delegate.first()
            result.experiment.description = self.ui.experimentDescriptionLineEdit.toPlainText()

        if self.field('isExistingDataset'):
            assert self.selected_existing_dataset is not None
            result.dataset = self.selected_existing_dataset
        else:
            result.dataset = Dataset()
            result.dataset._store = self.metadataModel.metadata
            result.dataset.dataset_name = self.ui.datasetNameLineEdit.text()
            result.dataset.identifiers_delegate.add(self.ui.datasetIDLineEdit.text())
            # Because a dataset can belong to multiple experiments,
            # we are creating a list around the experiment we captured.
            result.dataset.experiment_id = [result.experiment.identifiers_delegate.first()]
        result.file_list = []
        ### Create new Datafile object and append to result.datafile.files
        table = self.ui.datafiletableWidget
        image_processor = ImageProcessor()
        for row in range(table.rowCount()):
            datafile = Datafile()
            datafile._store = self.metadataModel.metadata
            datafile.dataset_id = result.dataset.identifiers_delegate.first()
            file_name = table.item(row,0).text()
            file_size: int = table.item(row,1).data(QtCore.Qt.ItemDataRole.UserRole)
            dir_path = Path(table.item(row, 2).text())
            datafile.filename = file_name
            datafile.size = file_size
            datafile.path_abs = dir_path
            # get image metadata and attach to datafile's metadata
            image_metadata = image_processor.get_metadata(dir_path.as_posix())
            datafile.metadata = image_metadata
            result.file_list.append(datafile)
        self.submitted.emit(result)