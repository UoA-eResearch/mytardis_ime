from PyQt5.QtWidgets import QWidget
from ime.models import GroupACL, IAccessControl, UserACL
from ime.ui.ui_project_access_control_tab import Ui_ProjectAccessControlTab
from ime.widgets.access_control_list import AccessControlList

class ProjectAccessControlTab(QWidget):

    _user_list: AccessControlList[UserACL]
    _group_list: AccessControlList[GroupACL]

    def __init__(self, parent = None):
        super().__init__(parent)
        ui = Ui_ProjectAccessControlTab()
        ui.setupUi(self)
        self.ui = ui
        ui.users.initialise_fields(UserACL)
        ui.groups.initialise_fields(GroupACL)
        self._user_list = ui.users
        self._group_list = ui.groups

    def set_data(self, data: IAccessControl):
        """Sets the MyTardis object `val` that this access control tab should display information for.
        Resets widgets to display information in `val`.

        Args:
            data (IAccessControl): Access control properties to display in this access control tab.
        """
        if data.users == None:
            data.users = []
        if data.groups == None:
            data.groups = []
        self._user_list.set_data(data.users)
        self._group_list.set_data(data.groups)
