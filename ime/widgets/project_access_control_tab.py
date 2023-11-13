from PyQt6.QtWidgets import QWidget
from ime.models import GroupACL, IAccessControl, UserACL
from ime.qt_models import DataclassTableModel
from ime.ui.ui_project_access_control_tab import Ui_ProjectAccessControlTab
from ime.widgets.access_control_list import AccessControlList

class ProjectAccessControlTab(QWidget):
    """
    Project-specific widget for access control tab.
    """
    _user_model: DataclassTableModel[UserACL]
    _group_model: DataclassTableModel[GroupACL]

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        ui = Ui_ProjectAccessControlTab()
        ui.setupUi(self)
        self.ui = ui
        # Set up the AccessControlLists.
        self._user_model = DataclassTableModel(UserACL)
        self._group_model = DataclassTableModel(GroupACL)
        ui.users.set_model(self._user_model)
        ui.groups.set_model(self._group_model)

    def set_data(self, data: IAccessControl) -> None:
        """Sets the MyTardis object `val` that this access control tab should display information for.
        Resets widgets to display information in `val`.

        Args:
            data (IAccessControl): Access control properties to display in this access control tab.
        """
        if data.users == None:
            data.users = []
        if data.groups == None:
            data.groups = []
        self._user_model.set_instance_list(data.users)
        self._group_model.set_instance_list(data.groups)