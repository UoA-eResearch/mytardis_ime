from typing import List
from PyQt5.QtWidgets import QWidget
from .ui_access_control_tab import Ui_AccessControlTab
from ime.models import IAccessControl
from ime.widgets.access_control_list import AccessControlList

class AccessControlTab(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.ui = Ui_AccessControlTab()
        self.ui.setupUi(self)        

    def set_has_inheritance(self, has_inheritance: bool):
        self.ui.adminGroupsList.set_has_inheritance(has_inheritance)
        self.ui.adminUsersList.set_has_inheritance(has_inheritance)
        self.ui.readGroupsList.set_has_inheritance(has_inheritance)
        self.ui.readUsersList.set_has_inheritance(has_inheritance)
        self.ui.downloadGroupsList.set_has_inheritance(has_inheritance)
        self.ui.downloadUsersList.set_has_inheritance(has_inheritance)
        self.ui.sensitiveGroupsList.set_has_inheritance(has_inheritance)
        self.ui.sensitiveUsersList.set_has_inheritance(has_inheritance)

    def set_item(self, ac_item: IAccessControl):
        self.ac_item = ac_item
        self.ui.adminGroupsList.set_list(ac_item.admin_groups)
        self.ui.adminUsersList.set_list(ac_item.admin_users)
        self.ui.readGroupsList.set_list(ac_item.read_groups)
        self.ui.readUsersList.set_list(ac_item.read_users)
        self.ui.downloadGroupsList.set_list(ac_item.download_groups)
        self.ui.downloadUsersList.set_list(ac_item.download_users)
        self.ui.sensitiveGroupsList.set_list(ac_item.sensitive_groups)
        self.ui.sensitiveUsersList.set_list(ac_item.sensitive_users)