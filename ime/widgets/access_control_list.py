from typing import List
import typing

from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, QObject, QSignalBlocker
from .ui_access_control_list import Ui_AccessControlList
from ime.qt_models import ListModel
from PyQt5.QtWidgets import QMessageBox, QWidget

class AccessControlList(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_AccessControlList()
        self.ui.setupUi(self)
        self.ui.btnAdd.clicked.connect(self.handle_insert_new)
        self.ui.btnDelete.clicked.connect(self.handle_remove)
        # To monitor focus out events and deselect
        # self.ui.aclList.installEventFilter(self)
        self.ui.overrideCheckBox.installEventFilter(self)
        self.ui.overrideCheckBox.setVisible(False)
        self.ui.overrideCheckBox.toggled.connect(self.handle_override_changed)
        self.has_inheritance = False

    def set_has_inheritance(self, has_inheritance: bool):
        self.has_inheritance = has_inheritance
        self.ui.overrideCheckBox.setVisible(has_inheritance)
        if not has_inheritance:
            self.ui.aclList.setEnabled(True)
        elif getattr(self, 'list_model', None) is None:
            self.ui.aclList.setDisabled(True)
            return
        elif self.list_model.rowCount() > 0:
            # TODO Need to differentiate no vs empty state
            self.ui.overrideCheckBox.setChecked(True)
            self.ui.aclList.setEnabled(True)
        else:
            self.ui.aclList.setDisabled(True)
            self.ui.overrideCheckBox.setChecked(False)

    def handle_override_changed(self):
        checked = self.ui.overrideCheckBox.isChecked()
        list_count = self.list_model.rowCount()
        if not checked and list_count > 0:
            msg = QMessageBox()
            msg.setWindowTitle("Use inherited value instead?")
            msg.setText("Are you sure you want to remove all users/groups from this field?")
            msg.setInformativeText("Inherited values will apply instead.")
            msg.setStandardButtons(typing.cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel))
            res = msg.exec()
            if res == QMessageBox.StandardButton.Cancel:
                with QSignalBlocker(self.ui.overrideCheckBox):
                    # Undo the check.
                    self.ui.overrideCheckBox.setChecked(True)
            else:
                # Remove all items in list
                self.list_model.removeRows(0, self.list_model.rowCount())
        # Finally, set to enable to disable the list
        self.ui.aclList.setEnabled(self.ui.overrideCheckBox.isChecked())


    def handle_insert_new(self):
        if getattr(self, 'list_model', None) is None:
            return
        idx = self.list_model.rowCount()
        self.list_model.insertRow(idx)
        model_idx = self.list_model.index(idx, 0)
        self.ui.aclList.setCurrentIndex(model_idx)
        self.ui.aclList.edit(model_idx)
        

    # def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
    #     # Clear selection if user clicks away
    #     self.ui.aclList.clearSelection()

    # def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
    #     if a0 is self.ui.overrideCheckBox and a1.type() == QEvent.Type.:
    #         print("Check box event!")
    #     return False

    def handle_remove(self):
        if getattr(self, 'list_model', None) is None:
            return
        idx_list = self.ui.aclList.selectedIndexes()
        values = [self.list_model.data(idx) for idx in idx_list]
        for val in values:
            self.list_model.remove_value(val)

    def set_list(self, ac_list: List[str]):
        self.list_model = ListModel(ac_list, self)
        self.ui.aclList.setModel(self.list_model)
        # Reapply in case this list has value
        self.set_has_inheritance(self.has_inheritance)