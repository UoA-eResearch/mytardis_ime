from dataclasses import field
from PyQt5.QtWidgets import QLineEdit, QWidget
from ime.bindable import BoundObject
from ime.models import Dataset, Experiment, FileInfo, Project
from ime.widgets.ui_dataset_props import Ui_DatasetProps
from ime.widgets.ui_datafile_props import Ui_DatafilePropertyEditor
from ime.widgets.ui_experiment_props import Ui_ExperimentPropertyEditor
from ime.widgets.ui_project_props import Ui_ProjectPropertyEditor
from ime.widgets.metadata_tab import MetadataTab

class DatasetPropertyEditor(QWidget):
    dataset: BoundObject[Dataset]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DatasetProps()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.page_3
        self.ui.accessControlTab.set_has_inheritance(True)

    def set_bound_dataset(self, dataset: BoundObject[Dataset]):
        self.dataset = dataset
        self.dataset.bind_input("dataset_name", self.ui.datasetNameLineEdit)
        self.dataset.bind_input("dataset_id", self.ui.datasetIDLineEdit)
        self.dataset.bind_input("instrument_id", self.ui.instrumentIDLineEdit)
        self.dataset.bound_object_changed.connect(self._handle_obj_changed)
    
    def _handle_obj_changed(self):
        self.metadata_tab.update_metadata_object(self.dataset._bound_object)
        self.ui.accessControlTab.set_item(self.dataset._bound_object)

    # def update_dataset(self, dataset: BoundObject[Dataset]):
    #     # self.ui.datasetNameLineEdit.setText(dataset.dataset_name)
    #     # self.ui.datasetNameLineEdit.textChanged.connect(lambda )
    #     if hasattr(self, "dataset"):
    #         self.dataset.unbind()
    #     self.dataset = dataset
    #     self.dataset.bind_input("dataset_name", self.ui.datasetNameLineEdit)
    #     self.dataset.bind_input("dataset_id", self.ui.datasetIDLineEdit)
    #     self.dataset.bind_input("instrument_id", self.ui.instrumentIDLineEdit)
    #     self.metadata_tab.update_metadata_object(dataset._bound_object)


class DatafilePropertyEditor(QWidget):
    file_info:BoundObject[FileInfo]
    metadata_tab: MetadataTab

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_DatafilePropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self.ui.accessControlTab.set_has_inheritance(True)

    def set_bound_file(self, file_info: BoundObject[FileInfo]):
        self.file_info = file_info
        self.file_info.bind_input("name", self.ui.fileInfoFilenameLineEdit)
        self.file_info.bound_object_changed.connect(self._handle_obj_changed)

    def _handle_obj_changed(self):
        self.metadata_tab.update_metadata_object(self.file_info._bound_object)
        self.ui.accessControlTab.set_item(self.file_info._bound_object)

class ExperimentPropertyEditor(QWidget):
    exp: BoundObject[Experiment]
    metadata_tab: MetadataTab

    def _bind_field(self, lineEdit: QLineEdit, field_name: str):
        lineEdit.setText(getattr(self.exp, field_name))
        lineEdit.textChanged.connect(lambda: setattr(self.exp, field_name, lineEdit.text()))

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ExperimentPropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self.ui.accessControlTab.set_has_inheritance(True)

    def set_bound_experiment(self, experiment: BoundObject[Experiment]):
        self.exp = experiment
        self.exp.bind_input("experiment_name", self.ui.experimentNameLineEdit)
        self.exp.bind_input("experiment_id", self.ui.experimentIDLineEdit)
        self.exp.bind_input("description", self.ui.experimentDescriptionLineEdit)
        self.exp.bound_object_changed.connect(self._handle_obj_changed)

    def _handle_obj_changed(self):
        self.metadata_tab.update_metadata_object(self.exp._bound_object)
        self.ui.accessControlTab.set_item(self.exp._bound_object)

class ProjectPropertyEditor(QWidget):
    project: BoundObject[Project]
    metadata_tab: MetadataTab

    def _bind_field(self, lineEdit: QLineEdit, field_name: str):
        lineEdit.setText(getattr(self.project, field_name))
        lineEdit.textChanged.connect(lambda: setattr(self.project, field_name, lineEdit.text()))

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProjectPropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self.ui.accessControlTab.set_has_inheritance(False)

    def set_bound_project(self, project: BoundObject[Project]):
        self.project = project
        self.project.bind_input("project_name", self.ui.projectNameLineEdit)
        self.project.bind_input("project_id", self.ui.projectIDLineEdit)
        self.project.bind_input("description", self.ui.projectDescriptionLineEdit)
        self.project.bind_input("lead_researcher", self.ui.leadResearcherLineEdit)
        self.project.bound_object_changed.connect(self._handle_obj_changed)

    def _handle_obj_changed(self):
        self.metadata_tab.update_metadata_object(self.project._bound_object)
        self.ui.accessControlTab.set_item(self.project._bound_object)
