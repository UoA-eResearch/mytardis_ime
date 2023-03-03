from PyQt5.QtWidgets import QWidget
from ime.bindable import BoundObject
from ime.models import Dataset, Experiment, FileInfo, Project
from ime.ui.ui_dataset_props import Ui_DatasetProps
from ime.ui.ui_datafile_props import Ui_DatafilePropertyEditor
from ime.ui.ui_experiment_props import Ui_ExperimentPropertyEditor
from ime.ui.ui_project_props import Ui_ProjectPropertyEditor
from ime.widgets.metadata_tab import MetadataTab

class DatasetPropertyEditor(QWidget):
    dataset: BoundObject[Dataset]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DatasetProps()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.page_3
        self._set_bound_dataset(BoundObject())

    def set_dataset(self, dataset: Dataset):
        self.dataset.set_object(dataset)
        self.metadata_tab.update_metadata_object(dataset)
        self.ui.accessControlTab.data = dataset

    def _set_bound_dataset(self, dataset: BoundObject[Dataset]):
        self.dataset = dataset
        self.dataset.bind_input("dataset_name", self.ui.datasetNameLineEdit)
        self.dataset.bind_input("dataset_id", self.ui.datasetIDLineEdit)
        self.dataset.bind_input("instrument_id", self.ui.instrumentIDLineEdit)

class DatafilePropertyEditor(QWidget):
    file_info:BoundObject[FileInfo]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DatafilePropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self._set_bound_file(BoundObject())

    def set_fileinfo(self, file_info: FileInfo):
        self.file_info.set_object(file_info)
        self.metadata_tab.update_metadata_object(file_info)
        self.ui.accessControlTab.data = file_info

    def _set_bound_file(self, file_info: BoundObject[FileInfo]):
        self.file_info = file_info
        self.file_info.bind_input("name", self.ui.fileInfoFilenameLineEdit)

class ExperimentPropertyEditor(QWidget):
    exp: BoundObject[Experiment]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ExperimentPropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self._set_bound_experiment(BoundObject())

    def set_experiment(self, experiment: Experiment):
        self.exp.set_object(experiment)
        self.metadata_tab.update_metadata_object(experiment)
        self.ui.accessControlTab.data = experiment

    def _set_bound_experiment(self, experiment: BoundObject[Experiment]):
        self.exp = experiment
        self.exp.bind_input("experiment_name", self.ui.experimentNameLineEdit)
        self.exp.bind_input("experiment_id", self.ui.experimentIDLineEdit)
        self.exp.bind_input("description", self.ui.experimentDescriptionLineEdit)

class ProjectPropertyEditor(QWidget):
    project: BoundObject[Project]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProjectPropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self._set_bound_project(BoundObject())

    def set_project(self, project: Project):
        self.project.set_object(project)
        self.metadata_tab.update_metadata_object(project)
        self.ui.accessControlTab.data = project

    def _set_bound_project(self, project: BoundObject[Project]):
        self.project = project
        self.project.bind_input("project_name", self.ui.projectNameLineEdit)
        self.project.bind_input("project_id", self.ui.projectIDLineEdit)
        self.project.bind_input("description", self.ui.projectDescriptionLineEdit)
        self.project.bind_input("lead_researcher", self.ui.leadResearcherLineEdit)  