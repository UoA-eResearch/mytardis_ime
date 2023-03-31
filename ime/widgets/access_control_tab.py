from dataclasses import dataclass, fields
from typing import List, Union, cast
from PyQt5.QtCore import QSignalBlocker
from PyQt5.QtWidgets import QMessageBox, QWidget
from ime.ui.ui_access_control_tab import Ui_AccessControlTab
from ime.models import IAccessControl, IProjectAccessControl, IDerivedAccessControl
from ime.widgets.access_control_list import AccessControlList, DerivedAccessControlListData, ProjectAccessControlListData
from functools import partial

class AccessControlTab(QWidget):
    """A custom QWidget for displaying and managing access control settings.
    
    Attributes:
    - ui (Ui_AccessControlTab): The user interface object.
    - views_by_field (dict): A dictionary mapping field names to the corresponding list views.
    
    Properties:
    - data: A property that returns the current access control data.
    
    Methods:
    - __init__(self, parent = None): Initializes the widget with the given parent and sets up the user interface.
    - display_confirm_reset_override_dialog(self) -> bool: Displays a message box asking the user to confirm resetting the override, and returns True if the user clicks "Ok".
    - handle_override_toggled(self, field: str, enabled: bool): Handles the "override_inherited_toggled" signal from the list views, and updates the corresponding access control field accordingly.
    """
    def __init__(self, parent = None):
        """Initializes the widget with the given parent and sets up the user interface."""
        super().__init__(parent)
        self.ui = Ui_AccessControlTab()
        self.ui.setupUi(self)
        # Maps field names to Qt widgets so we can display
        # the correct fields.
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
                partial(self._handle_override_toggled, field)
            )

    def data(self) -> IAccessControl:
        """Gets the currently displayed MyTardis object.

        Returns:
            IAccessControl: The currently displayed MyTardis object.
        """
        return self._data
    
    def set_data(self, val: IAccessControl):
        """Sets the MyTardis object `val` that this access control tab should display information for.
        Resets widgets to display information in `val`.

        Args:
            val (IAccessControl): The MyTardis object to display in this access control tab.
        """
        self._data = val
        for field in self.views_by_field:
            if isinstance(val, IProjectAccessControl): 
                data = ProjectAccessControlListData(getattr(val, field))
            elif isinstance(val, IDerivedAccessControl):
                # Currently the derived data list is a stub.
                data = DerivedAccessControlListData(getattr(val, field), [])
            self.views_by_field[field].set_data(data)

    def _display_confirm_reset_override_dialog(self) -> bool:
        """Private method for showing a dialogue confirming the user wishes to reset
        access control to use inherited values, losing all custom values.

        Returns:
            bool: True if the user wishes to reset access control, False if not. 
        """
        msg = QMessageBox()
        msg.setWindowTitle("Use inherited value instead?")
        msg.setText("Are you sure you want to remove all users/groups from this field?")
        msg.setInformativeText("Inherited values will apply instead.")
        msg.setStandardButtons(cast(QMessageBox.StandardButtons, QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel))
        res = msg.exec()
        return res == QMessageBox.StandardButton.Ok
    
    def _handle_override_toggled(self, field: str, enabled: bool):
        """Private method for handling if the override inherited checkbox is toggled.

        Args:
            field (str): Name of the field the checkbox is being toggled for.
            enabled (bool): The new state of the checkbox.
        """
        if enabled:
            # Add an empty array in the field, which represents overriding the
            # inherited field.
            setattr(self.data, field, [])
            # Using a stub empty array for the inherited_data parameter. We can
            # implement displaying inherited values in AccessControlList later.
            self.views_by_field[field].set_data(DerivedAccessControlListData(
                getattr(self.data, field), []
            ))
        else:
            if self._display_confirm_reset_override_dialog():
                # If we confirm the users wants to reset override
                # then reset the field by making it a None.
                setattr(self.data, field, None)
                # Using a stub empty array for the inherited_data parameter. We can
                # implement displaying inherited values in AccessControlList later.
                self.views_by_field[field].set_data(DerivedAccessControlListData(
                    getattr(self.data, field), []
                ))