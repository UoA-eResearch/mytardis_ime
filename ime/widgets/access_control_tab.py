from dataclasses import dataclass, fields
from typing import List, cast
from PyQt5.QtCore import QSignalBlocker
from PyQt5.QtWidgets import QMessageBox, QWidget
from ime.ui.ui_access_control_tab import Ui_AccessControlTab
from ime.models import IAccessControl, IOriginAccessControl, IDerivedAccessControl
from ime.widgets.access_control_list import AccessControlList, DerivedAccessControlData, OriginAccessControlData
from functools import partial

class AccessControlTab(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_AccessControlTab()
        self.ui.setupUi(self)
        self.views_by_field = {
            'admin_groups': self.ui.adminGroupsList,
            'admin_users': self.ui.adminUsersList,
            'read_groups': self.ui.readGroupsList,
            'read_users': self.ui.readUsersList,
            'download_groups': self.ui.downloadGroupsList,
            'download_users': self.ui.downloadUsersList,
            'sensitive_groups': self.ui.sensitiveGroupsList,
            'sensitive_users': self.ui.sensitiveUsersList
        }
        # Connect our handler to the override inherited signal (i.e. user
        # clicking the checkbox), using partial to include the field name.
        for field in self.views_by_field:
            self.views_by_field[field].override_inherited_toggled.connect(
                partial(self.handle_override_toggled, field)
            )

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, val: IAccessControl):
        self._data = val
        for field in self.views_by_field:
            if isinstance(val, IOriginAccessControl): 
                data = OriginAccessControlData(getattr(val, field))
            elif isinstance(val, IDerivedAccessControl):
                # Currently the derived data list is a stub.
                data = DerivedAccessControlData(getattr(val, field), [])
            self.views_by_field[field].data = data

    def display_confirm_reset_override_dialog(self) -> bool:
        msg = QMessageBox()
        msg.setWindowTitle("Use inherited value instead?")
        msg.setText("Are you sure you want to remove all users/groups from this field?")
        msg.setInformativeText("Inherited values will apply instead.")
        msg.setStandardButtons(cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel))
        res = msg.exec()
        return res == QMessageBox.StandardButton.Ok
    
    def handle_override_toggled(self, field: str, enabled: bool):
        if enabled:
            setattr(self.data, field, [])
            self.views_by_field[field].data = DerivedAccessControlData(
                getattr(self.data, field), []
            )
        else:
            if self.display_confirm_reset_override_dialog():
                # If we confirm the users wants to reset override
                # then reset the field.
                setattr(self.data, field, None)
                self.views_by_field[field].data = DerivedAccessControlData(
                    getattr(self.data, field), []
                )