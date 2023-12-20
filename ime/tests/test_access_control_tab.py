from typing import List
from PySide6.QtCore import QModelIndex, QPoint, QUrl, Qt
from PySide6.QtWidgets import QDataWidgetMapper, QDialog, QHeaderView, QLabel, QLineEdit, QListView, QTableView, QVBoxLayout, QWidget
from pytestqt.qtbot import QtBot
import pytest
from ime.blueprints.custom_data_types import Username
from ime.models import Experiment, IAccessControl, IngestionMetadata, Project, UserACL
from ime.widgets.access_control_list import AccessControlList
from ime.widgets.overridable_access_control_tab import OverridableAccessControlTab

from ime.widgets.project_access_control_tab import ProjectAccessControlTab


@pytest.fixture
def experiments(metadata: IngestionMetadata) -> List[Experiment]:
    return metadata.experiments

@pytest.fixture
def projects(metadata: IngestionMetadata):
    return metadata.projects

def test_show_project_access_control(qtbot: QtBot, projects: List[Project]):
    view = QDialog()
    project = projects[0]
    tab = ProjectAccessControlTab(view)
    tab.set_data(project)
    user_model = tab.ui.users.ui.aclTable.model()
    group_model = tab.ui.groups.ui.aclTable.model()
    assert user_model is not None
    assert group_model is not None
    assert user_model.rowCount() == 1
    assert user_model.data(user_model.index(0,0)) == "xli677"
    assert group_model.rowCount() == 1
    assert group_model.data(group_model.index(0,0)) == "biru-group1"

def test_show_overridable_access_control(qtbot: QtBot, experiments: List[Experiment]):
    """Tests access control tab can be created."""
    view = QDialog()
    experiment = experiments[0]
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, IAccessControl())
    user_model = tab.ui.users.ui.aclTable.model()
    group_model = tab.ui.groups.ui.aclTable.model()
    assert user_model is not None
    assert group_model is not None
    assert user_model.rowCount() == 2
    assert group_model.rowCount() == 2
    test_admin_is_owner = user_model.data(user_model.index(0,1),Qt.ItemDataRole.CheckStateRole)
    assert test_admin_is_owner == Qt.CheckState.Checked


def test_project_ac_creates_new_list_if_none(qtbot: QtBot,):
    view = QDialog()
    # Create a blank project, 
    # then check that a new list is created.
    project = Project()
    assert project.users is None
    assert project.groups is None
    tab = ProjectAccessControlTab(view)
    tab.set_data(project)
    assert project.users is not None
    assert project.groups is not None
    
def test_edit_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    """Test for editing an access control field results in changes in underlying model."""
    view = QDialog()
    experiment = experiments[0]
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, IAccessControl())
    model = tab.ui.users.ui.aclTable.model()
    assert model is not None
    edit_location = model.index(0,0)
    assert model.data(edit_location, Qt.ItemDataRole.DisplayRole) == "xli677"
    edit_location = model.index(0,0)
    model.setData(edit_location,"Testing editing")
    assert experiment.users is not None
    assert experiment.users[0].user == "Testing editing"

def test_add_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    view = QDialog()
    experiment = experiments[0]
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, IAccessControl())
    model = tab.ui.users.ui.aclTable.model()
    assert model is not None
    assert model.rowCount() == 2
    tab.ui.users.ui.btnAdd.click()
    qtbot.wait(100)
    # Check there's increased number of rows.
    assert model.rowCount() == 3
    edit_location = model.index(2,0)
    model.setData(edit_location,"New user")
    qtbot.wait(100)
    # Check that UI changes are reflected in model
    assert experiment.users is not None
    assert len(experiment.users) == 3
    assert experiment.users[2].user == "New user"

def test_delete_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    view = QDialog()
    experiment = experiments[0]
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, IAccessControl())
    assert experiment.users is not None
    old_length = len(experiment.users)
    name_to_delete = experiment.users[0].user
    index_to_delete = tab.ui.users._model.index(0,0)
    tab.ui.users.ui.aclTable.setCurrentIndex(index_to_delete)
    tab.ui.users.ui.btnDelete.click()
    qtbot.wait(100)
    # Check there's one less user
    assert len(experiment.users) == old_length - 1
    # Check the deleted name is no longer in list.
    assert name_to_delete not in [acl.user for acl in experiment.users]
    assert tab.ui.users._model.rowCount() == old_length - 1

def test_overridable_list_show_inherited_data_if_data_is_none(qtbot: QtBot):
    view = QDialog()
    # Empty experiment which won't have any user access control.
    experiment = Experiment()
    inherited = IAccessControl(
        [UserACL(Username("inherited"), True, False, False)]
    )
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, inherited)
    model = tab.ui.users._model 
    assert model.rowCount() == 1
    name_location = model.index(0,0)
    assert model.data(name_location) == "inherited"

def test_overridable_list_show_data_if_data_is_empty_list(qtbot: QtBot):
    view = QDialog()
    # An empty list is an override. Distinct from None.
    experiment = Experiment(users=[])
    inherited = IAccessControl(
        [UserACL(Username("inherited"), True, False, False)]
    )
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, inherited)
    model = tab.ui.users._model 
    assert model.rowCount() == 0
    assert tab.ui.usersOverride.isChecked()

def test_access_control_edit_works(qtbot: QtBot):
    """Tests whether the access control checkboxes work. """
    view = QDialog()
    acl = UserACL(user=Username("szen012"))
    project = Project(users=[acl])
    tab = ProjectAccessControlTab(view)
    tab.set_data(project)
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    # Find the coordinate of the checkmark for is owner and click it.
    user_table = tab.ui.users.ui.aclTable
    is_owner_checkbox = user_table.visualRect(user_table.model().index(0,1)).center()
    viewport = user_table.viewport()
    qtbot.mouseClick(viewport, Qt.MouseButton.LeftButton, pos=is_owner_checkbox)
    qtbot.wait(100)
    # New check the underlying access control property is changed.
    assert acl.is_owner is True
