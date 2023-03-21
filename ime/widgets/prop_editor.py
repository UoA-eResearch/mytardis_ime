from PyQt5.QtWidgets import QWidget
from ime.bindable import BoundObject
from ime.models import Dataset, Experiment, Datafile, FileInfo, Project
from ime.ui.ui_dataset_props import Ui_DatasetProps
from ime.ui.ui_datafile_props import Ui_DatafilePropertyEditor
from ime.ui.ui_experiment_props import Ui_ExperimentPropertyEditor
from ime.ui.ui_project_props import Ui_ProjectPropertyEditor
from ime.widgets.metadata_tab import MetadataTab

class DatasetPropertyEditor(QWidget):
    dataset: BoundObject[Dataset]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        """
        Constructs a new instance of the DatasetPropertyEditor class.
        
        Args:
        parent: Optional parent widget of this widget.
        """
        super().__init__(parent)
        self.ui = Ui_DatasetProps()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.page_3
        self._set_bound_dataset(BoundObject())

    def set_dataset(self, dataset: Dataset):
        """
        Sets the current `Dataset` to edit in this widget.
        
        Args:
        dataset: The `Dataset` to edit.
        """
        self.dataset.set_object(dataset)
        self.metadata_tab.update_metadata_object(dataset)
        self.ui.accessControlTab.data = dataset

    def _set_bound_dataset(self, dataset: BoundObject[Dataset]):
        """
        Binds a `BoundObject` to this editor to keep its properties synchronized with the UI.
        
        Args:
        dataset: The `BoundObject` to bind to this editor.
        """
        self.dataset = dataset
        self.dataset.bind_input("dataset_name", self.ui.datasetNameLineEdit)
        self.dataset.bind_input("dataset_id", self.ui.datasetIDLineEdit)
        self.dataset.bind_input("instrument_id", self.ui.instrumentIDLineEdit)

class DatafilePropertyEditor(QWidget):
    ### change variable names to create new Datafile

    df:BoundObject[Datafile]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        """
        Constructs a new instance of the DatafilePropertyEditor class.
        
        Args:
        parent: Optional parent widget of this widget.
        """
        super().__init__(parent)
        self.ui = Ui_DatafilePropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self._set_bound_file(BoundObject())
    ### create new Datafile
    def set_datafile(self, datafile: Datafile):
        """
        Sets the current `Datafile` to edit in this widget.
        
        Args:
        datafile: The `Datafile` to edit.
        """
        self.df.set_object(datafile)
        self.metadata_tab.update_metadata_object(datafile)
        self.ui.accessControlTab.set_item(datafile)
    
    def _set_bound_file(self, datafile: BoundObject[Datafile]):
        """
        Binds a `BoundObject` to this editor to keep its properties synchronized with the UI.
        
        Args:
        datafile: The `BoundObject` to bind to this editor.
        """
        self.df = datafile
        self.df.bind_input("name", self.ui.fileInfoFilenameLineEdit)
    '''
    ### comment out fileinfo
    def set_fileinfo(self, file_info: FileInfo):
        self.file_info.set_object(file_info)
        self.metadata_tab.update_metadata_object(file_info)
        self.ui.accessControlTab.data = file_info

    def _set_bound_file(self, file_info: BoundObject[FileInfo]):
        self.file_info = file_info
        self.file_info.bind_input("name", self.ui.fileInfoFilenameLineEdit)
    '''

class ExperimentPropertyEditor(QWidget):
    exp: BoundObject[Experiment]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        """Initialize an ExperimentPropertyEditor object.

        Args:
            parent: Parent widget (default None).
        """
        super().__init__(parent)
        self.ui = Ui_ExperimentPropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self._set_bound_experiment(BoundObject())

    def set_experiment(self, experiment: Experiment):
        """Set the current experiment.

        Args:
            experiment: The experiment to be set.
        """
        self.exp.set_object(experiment)
        self.metadata_tab.update_metadata_object(experiment)
        self.ui.accessControlTab.data = experiment

    def _set_bound_experiment(self, experiment: BoundObject[Experiment]):
        """Set a bound object for the experiment.

        Args:
            experiment: The experiment object to be bound.
        """
        self.exp = experiment
        self.exp.bind_input("title", self.ui.experimentNameLineEdit)
        self.exp.bind_input("experiment_id", self.ui.experimentIDLineEdit)
        self.exp.bind_input("description", self.ui.experimentDescriptionLineEdit)

class ProjectPropertyEditor(QWidget):
    project: BoundObject[Project]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        """
        Constructor for the ProjectPropertyEditor class.

        Args:
            parent (QWidget): The parent widget (default is None).
        """
        super().__init__(parent)
        self.ui = Ui_ProjectPropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self._set_bound_project(BoundObject())

    def set_project(self, project: Project):
        """
        Sets the `Project` object for the editor.

        Args:
            project (Project): The `Project` object to set.
        """
        self.project.set_object(project)
        self.metadata_tab.update_metadata_object(project)
        self.ui.accessControlTab.data = project

    def _set_bound_project(self, project: BoundObject[Project]):
        """
        Binds the `Project` object to the UI elements.

        Args:
            project (BoundObject[Project]): The `Project` object to bind.
        """
        self.project = project
        self.project.bind_input("name", self.ui.projectNameLineEdit)
        self.project.bind_input("project_id", self.ui.projectIDLineEdit)
        self.project.bind_input("description", self.ui.projectDescriptionLineEdit)
        self.project.bind_input("lead_researcher", self.ui.leadResearcherLineEdit)  