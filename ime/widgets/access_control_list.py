from dataclasses import dataclass, field
from typing import List, Optional, TypeAlias, TypeVar, Union
import typing

from PyQt5.QtCore import QSignalBlocker, pyqtSignal
from ime.qt_models import PythonListModel
from ime.ui.ui_access_control_list import Ui_AccessControlList
from PyQt5.QtWidgets import QMessageBox, QWidget

@dataclass
class ProjectAccessControlListData:
    """Class for use with AccessControlList.data to represent access control data for MyTardis
    Project objects.
    To use, create a ProjectAccessControlData, passing in the Project instance
    """
    data: List[str] = field(default_factory=list)

@dataclass
class DerivedAccessControlListData:
    """Class for use with AccessControlList.data to represent access control data for MyTardis objects that have
    inherited access control - i.e. Experiments, Datasets and Datafiles. 
    """
    data: Optional[List[str]] = None
    inherited_data: List[str] = field(default_factory=list)

AccessControlListData:TypeAlias = Union[ProjectAccessControlListData, DerivedAccessControlListData]

class AccessControlList(QWidget):
    """
    Qt widget for the access control list widget. 
    """
    _model: PythonListModel
    is_overriding_inheritance: bool = False
    override_inherited_toggled = pyqtSignal(bool, name="overrideInheritedChanged")

    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_AccessControlList()
        self.ui.setupUi(self)
        self._model = PythonListModel(self)
        self.ui.aclList.setModel(self._model)
        self.ui.btnAdd.clicked.connect(self._handle_insert_new)
        self.ui.btnDelete.clicked.connect(self._handle_remove)
        # To monitor focus out events and deselect
        self.ui.overrideCheckBox.installEventFilter(self)
        self.ui.overrideCheckBox.toggled.connect(self._handle_override_checkbox_changed)
        self.set_data(ProjectAccessControlListData())

    def data(self) -> AccessControlListData:
        """Returns the currently displayed access control data.

        Returns:
            Union[OriginAccessControlData, DerivedAccessControlData]: The access control data
            being displayed.
        """
        return self._data

    def set_data(self, value: AccessControlListData):
        """
        Sets the access control data that will be displayed by the widget, and resets the widget interface
        using this data.
        
        Args:
            value (Union[OriginAccessControlData, DerivedAccessControlData]): _description_
        """
        self._data = value
        if isinstance(value, ProjectAccessControlListData):
            # If this is origin access control data (i.e. access control values from a Project)
            # then hide the override checkbox and show the values.
            self._model.setStringList(value.data)
            self.ui.overrideCheckBox.setVisible(False)
        elif isinstance(value, DerivedAccessControlListData):
            # If this is derived access control data(i.e. access control values from an Experiment,
            # Dataset or FileInfo), then show override checkbox and display values depending on
            # whether override values are available.
            self.ui.overrideCheckBox.setVisible(True)
            if value.data is None:
                # Disable editing, display inherited access controls.
                self._model.setStringList(value.inherited_data)
                self.ui.aclList.setEnabled(False)
                with QSignalBlocker(self.ui.overrideCheckBox):
                    self.ui.overrideCheckBox.setChecked(False)
            else:
                # Enable editing, display own access controls
                self._model.setStringList(value.data)
                self.ui.aclList.setEnabled(True)
                with QSignalBlocker(self.ui.overrideCheckBox):
                    self.ui.overrideCheckBox.setChecked(True)

    def _handle_override_checkbox_changed(self):
        """Private method for handling when "override" checkbox state is changed
        """
        is_overriding = self.ui.overrideCheckBox.isChecked()
        # Cancel the checkbox state change as we want to control
        # the change through the data property setter
        with QSignalBlocker(self.ui.overrideCheckBox):
            self.ui.overrideCheckBox.setChecked(not is_overriding)
        self.override_inherited_toggled.emit(is_overriding)

    def _handle_insert_new(self):
        """Private method for handling new user/group button clicked.
        """
        idx = self._model.rowCount()
        self._model.insertRow(idx)
        model_idx = self._model.index(idx, 0)
        self.ui.aclList.setCurrentIndex(model_idx)
        self.ui.aclList.edit(model_idx)

    def _handle_remove(self):
        """Private method for handling remove user/group button clicked.
        """
        idx_list = self.ui.aclList.selectedIndexes()
        rows_to_remove = [idx.row() for idx in idx_list]
        # Reverse sort the rows to remove, so we're not affected
        # by row index changes.
        rows_to_remove.sort(reverse=True)
        for row in rows_to_remove:
            self._model.removeRow(row)