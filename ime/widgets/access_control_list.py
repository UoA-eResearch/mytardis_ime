from dataclasses import dataclass, field
from typing import List, Optional, TypeVar, Union
import typing

from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, QObject, QSignalBlocker, pyqtSignal
from ime.qt_models import PythonListModel
from ime.ui.ui_access_control_list import Ui_AccessControlList
from PyQt5.QtWidgets import QMessageBox, QWidget, QLineEdit

@dataclass
class OriginAccessControlData:
    data: List[str] = field(default_factory=list)

@dataclass
class DerivedAccessControlData:
    data: Optional[List[str]] = None
    inherited_data: List[str] = field(default_factory=list)

class AccessControlList(QWidget):
    _model: PythonListModel
    is_overriding_inheritance: bool = False
    override_inherited_toggled = pyqtSignal(bool, name="overrideInheritedChanged")

    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_AccessControlList()
        self.ui.setupUi(self)
        self._model = PythonListModel(self)
        self.ui.aclList.setModel(self._model)
        self.ui.btnAdd.clicked.connect(self.handle_insert_new)
        self.ui.btnDelete.clicked.connect(self.handle_remove)
        # To monitor focus out events and deselect
        self.ui.overrideCheckBox.installEventFilter(self)
        self.ui.overrideCheckBox.toggled.connect(self.handle_override_checkbox_changed)
        self.data = OriginAccessControlData()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value: Union[OriginAccessControlData, DerivedAccessControlData]):
        self._data = value
        if isinstance(value, OriginAccessControlData):
            # If this is origin access control data (i.e. access control values from a Project)
            # then hide the override checkbox and show the values.
            self._model.setStringList(value.data)
            self.ui.overrideCheckBox.setVisible(False)
        elif isinstance(value, DerivedAccessControlData):
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

    def handle_override_checkbox_changed(self):
        is_overriding = self.ui.overrideCheckBox.isChecked()
        # Cancel the checkbox state change as we want to control
        # the change through the data property setter
        with QSignalBlocker(self.ui.overrideCheckBox):
            self.ui.overrideCheckBox.setChecked(not is_overriding)
        self.override_inherited_toggled.emit(is_overriding)

    def handle_insert_new(self):
        idx = self._model.rowCount()
        self._model.insertRow(idx)
        model_idx = self._model.index(idx, 0)
        self.ui.aclList.setCurrentIndex(model_idx)
        self.ui.aclList.edit(model_idx)

    def handle_remove(self):
        idx_list = self.ui.aclList.selectedIndexes()
        rows_to_remove = [idx.row() for idx in idx_list]
        # Reverse sort the rows to remove, so we're not affected
        # by row index changes.
        rows_to_remove.sort(reverse=True)
        for row in rows_to_remove:
            self._model.removeRow(row)
