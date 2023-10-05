from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5.uic import loadUi
from ime.bindable import BoundObject
from ime.models import Dataset, Experiment, Datafile, IAccessControl, Project, DataStatus
from ime.qt_models import PythonListModel
from ime.ui.ui_dataset_props import Ui_DatasetProps
from ime.ui.ui_datafile_props import Ui_DatafilePropertyEditor
from ime.ui.ui_experiment_props import Ui_ExperimentPropertyEditor
from ime.ui.ui_project_props import Ui_ProjectPropertyEditor
from ime.ui.ui_metadata_tab import Ui_MetadataTab
from ime.widgets.metadata_tab import MetadataTab

class DatasetPropertyEditor(QWidget):
    dataset: BoundObject[Dataset]
    metadata_tab: MetadataTab
    identifiers_model: PythonListModel

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
    
    def set_dataset(self, dataset: Dataset) -> None:
        """
        Sets the current `Dataset` to edit in this widget.
        
        Args:
        dataset: The `Dataset` to edit.
        """
        self.dataset.set_object(dataset)
        self.ui.identifierList.set_data(dataset.identifiers_delegate)
        if dataset.data_status == DataStatus.INGESTED.value:
            self.ui.page.setEnabled(False)
            self.ui.page_2.setEnabled(False)
            self.ui.page_3.setEnabled(False)
        else:
            self.ui.page.setEnabled(True)
            self.ui.page_2.setEnabled(True)
            self.ui.page_3.setEnabled(True)
        self.metadata_tab.update_metadata_object(dataset)
        inherited_acl = IAccessControl() # Stub - empty list.
        self.ui.accessControlTab.set_data(dataset, inherited_acl)
        
    def _set_bound_dataset(self, dataset: BoundObject[Dataset]) -> None:
        """
        Binds a `BoundObject` to this editor to keep its properties synchronized with the UI.
        
        Args:
        dataset: The `BoundObject` to bind to this editor.
        """
        self.dataset = dataset
        self.dataset.bind_input("description", self.ui.datasetNameLineEdit)
        self.dataset.bind_input("instrument_identifier", self.ui.instrumentIDLineEdit)

class DatafilePropertyEditor(QWidget):
    df:BoundObject[Datafile]
    metadata_tab: MetadataTab

    def __init__(self, parent=None) -> None:
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
    def set_datafile(self, datafile: Datafile) -> None:
        """
        Sets the current `Datafile` to edit in this widget.
        
        Args:
        datafile: The `Datafile` to edit.
        """
        self.df.set_object(datafile)
        if datafile.data_status == DataStatus.INGESTED.value:
            self.ui.fileinfoDescription.setEnabled(False)
            self.ui.page_10.setEnabled(False)
            self.ui.metadata_tab.setEnabled(False)
        else:
            self.ui.fileinfoDescription.setEnabled(True)
            self.ui.page_10.setEnabled(True)
            self.ui.metadata_tab.setEnabled(True)
        self.metadata_tab.update_metadata_object(datafile)
        inherited_acl = IAccessControl() # Stub - empty list.
        self.ui.accessControlTab.set_data(datafile, inherited_acl)
    
    def _set_bound_file(self, datafile: BoundObject[Datafile]) -> None:
        """
        Binds a `BoundObject` to this editor to keep its properties synchronized with the UI.
        
        Args:
        datafile: The `BoundObject` to bind to this editor.
        """
        self.df = datafile
        self.df.bind_input("filename", self.ui.fileInfoFilenameLineEdit)


class ExperimentPropertyEditor(QWidget):
    exp: BoundObject[Experiment]
    metadata_tab: MetadataTab

    def __init__(self, parent=None) -> None:
        """Initialize an ExperimentPropertyEditor object.

        Args:
            parent: Parent widget (default None).
        """
        super().__init__(parent)
        self.ui = Ui_ExperimentPropertyEditor()
        self.ui.setupUi(self)
        self.metadata_tab = self.ui.metadata_tab
        self._set_bound_experiment(BoundObject())

    def set_experiment(self, experiment: Experiment) -> None:
        """Set the current experiment.

        Args:
            experiment: The experiment to be set.
        """
        self.exp.set_object(experiment)
        self.ui.identifierList.set_data(experiment.identifiers_delegate)
        if experiment.data_status == DataStatus.INGESTED.value:
            self.ui.page_4.setEnabled(False)
            self.ui.page_5.setEnabled(False)
            self.ui.metadata_tab.setEnabled(False)
        else:
            self.ui.page_4.setEnabled(True)
            self.ui.page_5.setEnabled(True)
            self.ui.metadata_tab.setEnabled(True)
        self.metadata_tab.update_metadata_object(experiment)
        inherited_acl = IAccessControl() # Stub - empty list.
        self.ui.accessControlTab.set_data(experiment, inherited_acl)

    def _set_bound_experiment(self, experiment: BoundObject[Experiment]) -> None:
        """Set a bound object for the experiment.

        Args:
            experiment: The experiment object to be bound.
        """
        self.exp = experiment
        self.exp.bind_input("title", self.ui.experimentNameLineEdit)
        self.exp.bind_input("description", self.ui.experimentDescriptionLineEdit)

class ProjectPropertyEditor(QWidget):
    project: BoundObject[Project]
    metadata_tab: MetadataTab

    def __init__(self, parent=None) -> None:
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

    def set_project(self, project: Project) -> None:
        """
        Sets the `Project` object for the editor.

        Args:
            project (Project): The `Project` object to set.
        """
        self.project.set_object(project)
        self.ui.identifierList.set_data(project.identifiers_delegate)
        if project.data_status == DataStatus.INGESTED.value:
            self.ui.page_7.setEnabled(False)
            self.ui.page_8.setEnabled(False)
            self.ui.metadata_tab.setEnabled(False)
        else:
            self.ui.page_7.setEnabled(True)
            self.ui.page_8.setEnabled(True)
            self.ui.metadata_tab.setEnabled(True)
        self.metadata_tab.update_metadata_object(project)
        self.ui.accessControlTab.set_data(project)

    def _set_bound_project(self, project: BoundObject[Project]) -> None:
        """
        Binds the `Project` object to the UI elements.

        Args:
            project (BoundObject[Project]): The `Project` object to bind.
        """
        self.project = project
        self.project.bind_input("name", self.ui.projectNameLineEdit)
        self.project.bind_input("description", self.ui.projectDescriptionLineEdit)
        self.project.bind_input("principal_investigator", self.ui.leadResearcherLineEdit)
