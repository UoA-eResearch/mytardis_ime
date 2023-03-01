from typing import List
import typing

from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, QObject, QSignalBlocker, QStringListModel
from ime.ui.ui_access_control_list import Ui_AccessControlList
from PyQt5.QtWidgets import QMessageBox, QWidget, QLineEdit

class AccessControlList(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_AccessControlList()
        self.ui.setupUi(self)
        #Libby to add line edit
        #self.ui.input_box = QLineEdit(self)

        #Libby Initialize the flag to False
        self.item_added = False

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
        ### Libby to add text value to the listmodel
    
        checked = self.ui.overrideCheckBox.isChecked()
        if checked and (not self.item_added):
            row = self.list_model.rowCount() # get the number of rows in model --> int
            self.list_model.insertRows(row,1) # Enable add one or more row.
            model_idx = self.list_model.index(row)
            self.ui.aclList.setCurrentIndex(model_idx)
            self.ui.aclList.edit(model_idx)
            # Set the flag to True after an item has been added
            self.item_added = True

        # If an item has been added, remove any empty or null strings from the model
        elif checked and (self.item_added):
            self.remove_empty_strings(self.list_model)
            row = self.list_model.rowCount() # get the number of rows in model --> int
            self.list_model.insertRows(row,1) # Enable add one or more row.
            model_idx = self.list_model.index(row)
            self.ui.aclList.setCurrentIndex(model_idx)
            self.ui.aclList.edit(model_idx)
            self.item_added = True


    def handle_remove(self):
        if getattr(self, 'list_model', None) is None:
            return
        idx_list = self.ui.aclList.selectedIndexes()
        rows_to_remove = [idx.row() for idx in idx_list]
        # Reverse sort the rows to remove, so we're not affected
        # by row index changes.
        rows_to_remove.sort(reverse=True)
        for row in rows_to_remove:
            self.list_model.removeRow(row)

    def set_list(self, ac_list: List[str]):
        self.list_model = QStringListModel(self) # create stringlistmodel object
        self.list_model.setStringList(ac_list)  # assign values to the model
        self.ui.aclList.setModel(self.list_model) # connect view and model
        # Reapply in case this list has value
        self.set_has_inheritance(self.has_inheritance)

    def remove_empty_strings(self,model):
        # Get the string list from the model
        string_list = model.stringList()

        # Iterate through the string list and remove any empty or null strings
        for i in reversed(range(len(string_list))):
            if string_list[i] == '' or string_list[i] is None:
                model.removeRows(i, 1)