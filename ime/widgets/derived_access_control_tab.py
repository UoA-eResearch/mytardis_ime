from typing import cast
from PyQt5.QtCore import QSignalBlocker
from PyQt5.QtWidgets import QCheckBox, QMessageBox, QWidget
from ime.ui.ui_derived_access_control_tab import Ui_DerivedAccessControlTab
from ime.models import GroupACL, IAccessControl, UserACL


from ime.widgets.access_control_list import AccessControlList

class DerivedAccessControlTab(QWidget):
    """
    Widget for access control tab for Experiment, Dataset and Datafile.
    Includes a checkbox to override inherited properties.
    Methods:
    - __init__(self, parent = None): Initializes the widget with the given parent and sets up the user interface.
    - display_confirm_reset_override_dialog(self) -> bool: Displays a message box asking the user to confirm resetting the override, and returns True if the user clicks "Ok".
    - handle_override_toggled(self, field: str, enabled: bool): Handles the "override_inherited_toggled" signal from the list views, and updates the corresponding access control field accordingly.
    """
    _data: IAccessControl
    _inherited_data: IAccessControl
    _user_list: AccessControlList[UserACL]
    _group_list: AccessControlList[GroupACL]

    def __init__(self, parent = None):
        """Initializes the widget with the given parent and sets up the user interface."""
        super().__init__(parent)
        ui = Ui_DerivedAccessControlTab()
        ui.setupUi(self)
        self.ui = ui
        # Set up handling overrides.
        ui.usersOverride.toggled.connect(
            self._handle_users_override_toggled
        )
        ui.groupsOverride.toggled.connect(
            self._handle_groups_override_toggled
        )
        # Set up the AccessControlLists.
        ui.users.initialise_fields(UserACL)
        ui.groups.initialise_fields(GroupACL)
        self._user_list = ui.users
        self._group_list = ui.groups
        
    def _reset_checkbox(self, check_box: QCheckBox, value: bool) -> None:
        """A private method for resetting checkbox state without triggering any signals

        Args:
            check_box (QCheckBox): The checkbox to reset value for.
            value (bool): The new check state for the checkbox.
        """
        with QSignalBlocker(check_box):
            check_box.setChecked(value)
    
    def set_data(self, data: IAccessControl, inherited_data: IAccessControl):
        """Sets the MyTardis object `val` that this access control tab should display information for.
        Resets widgets to display information in `val`.

        Args:
            data (IAccessControl): Access control properties to display in this access control tab.
            inherited_data (IAccessControl): Inherited access control.
        """
        self._data = data
        self._inherited_data = inherited_data
        ui = self.ui
        # Check if there is override access control values.
        has_users_override = data.users is not None
        has_groups_override = data.groups is not None
        # Reset checkbox states.
        self._reset_checkbox(ui.usersOverride, has_users_override)
        self._reset_checkbox(ui.groupsOverride, has_groups_override)
        # Reset whether the access control lists can be changed.
        ui.users.set_disabled(not has_users_override)
        ui.groups.set_disabled(not has_groups_override)
        # Show override user/group access control if it exists,
        # otherwise show inherited access control.
        if data.users is not None:
            user_ac = data.users
        else:
            user_ac = inherited_data.users or []
        if data.groups is not None:
            group_ac = data.groups
        else:
            group_ac = inherited_data.groups or []
        # Set data for the AccessControlList widgets.
        self._user_list.set_data(user_ac)
        self._group_list.set_data(group_ac)

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
    
    def _handle_users_override_toggled(self, enabled: bool):
        """Private method for handling when the override checkbox
        is checked.

        Args:
            enabled (bool): Whether the override checkbox is checked.
        """
        if enabled:
            # Add an empty array in the field, which represents overriding the
            # inherited field.
            ac_list = []
            setattr(self._data, "users", ac_list)
            self._user_list.set_data(ac_list)
            self._user_list.set_disabled(False)
        else:
            # Only confirm unchecking this checkbox if user confirms.
            is_confirmed = self._display_confirm_reset_override_dialog()
            if not is_confirmed:
                # Reset the checkbox so it still shows overriding.
                self._reset_checkbox(self.ui.usersOverride, True)
            else:
                setattr(self._data, "users", None)
                self._user_list.set_data(self._inherited_data.users or [])
                self._user_list.set_disabled(True)

    def _handle_groups_override_toggled(self, enabled: bool):
        if enabled:
            # Add an empty array in the field, which represents overriding the
            # inherited field.
            ac_list = []
            setattr(self._data, "groups", ac_list)
            self._group_list.set_data(ac_list)
            self._group_list.set_disabled(False)
        else:
            # Only confirm unchecking this checkbox if user confirms.
            is_confirmed = self._display_confirm_reset_override_dialog()
            if not is_confirmed:
                # Reset the checkbox so it still shows overriding.
                self._reset_checkbox(self.ui.groupsOverride, True)
            else:
                setattr(self._data, "groups", None)
                self._group_list.set_data(self._inherited_data.groups or [])
                self._group_list.set_disabled(True)