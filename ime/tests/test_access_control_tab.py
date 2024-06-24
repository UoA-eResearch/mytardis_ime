from typing import List
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from pytestqt.qtbot import QtBot
import pytest
from ime.models import Experiment, IAccessControl, IngestionMetadata, Project, GroupACL
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
    group_model = tab.ui.groups.ui.aclTable.model()
    assert group_model is not None, "ACL table model should not be None."
    assert group_model.rowCount() == 1, "ACL table should have one row."
    assert group_model.data(group_model.index(0,0)) == "biru-group1", "First row should have group name 'biru-group1'."

def test_show_overridable_access_control(qtbot: QtBot, experiments: List[Experiment]):
    """Tests access control tab can be created."""
    view = QDialog()
    experiment = experiments[0]
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, IAccessControl())
    group_model = tab.ui.groups.ui.aclTable.model()
    assert group_model is not None, "ACL table model should not be None."
    assert group_model.rowCount() == 2, "ACL table should have two rows."

def test_project_ac_creates_new_list_if_none(qtbot: QtBot,):
    view = QDialog()
    # Create a blank project, 
    # then check that a new list is created.
    project = Project()
    assert project.groups is None, "Project should have no groups."
    tab = ProjectAccessControlTab(view)
    tab.set_data(project)
    assert project.groups is not None, "Groups list should be initialized after setting data."

def test_edit_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    """Test for editing an access control field results in changes in underlying model."""
    view = QDialog()
    experiment = experiments[0]
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, IAccessControl())
    acl_table = tab.ui.groups.ui.aclTable
    model = acl_table.model()
    assert model is not None, "ACL table model should not be None."
    edit_location = model.index(0,0)
    assert model.data(edit_location, Qt.ItemDataRole.DisplayRole) == "biru-group1"
    model.setData(edit_location,"Testing editing")
    assert experiment.groups[0].group == "Testing editing"

def test_add_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    view = QDialog()
    experiment = experiments[0]
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, IAccessControl())
    acl_table = tab.ui.groups.ui.aclTable
    model = acl_table.model()
    assert model is not None, "ACL table model should not be None."
    assert model.rowCount() == 2, "ACL table should have two rows."
    tab.ui.groups.ui.btnAdd.click()
    qtbot.wait(100)
    # Check there's increased number of rows.
    assert model.rowCount() == 3
    new_group_location = model.index(2,0)
    model.setData(new_group_location,"New group")
    qtbot.wait(100)
    # Check that UI changes are reflected in model
    assert experiment.groups[2].group == "New group"

def test_delete_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    view = QDialog()
    experiment = experiments[0]
    tab = OverridableAccessControlTab(view)
    tab.set_data(experiment, IAccessControl())
    acl_table = tab.ui.groups.ui.aclTable
    assert experiment.groups is not None
    old_length = len(experiment.groups)
    name_to_delete = experiment.groups[0].group
    index_to_delete = acl_table.model().index(0,0)
    acl_table.setCurrentIndex(index_to_delete)
    tab.ui.groups.ui.btnDelete.click()
    qtbot.wait(100)
    # Check there's one less user
    assert len(experiment.groups) == old_length - 1
    # Check the deleted name is no longer in list.
    assert name_to_delete not in [acl.group for acl in experiment.groups]
    assert acl_table.model().rowCount() == old_length - 1

def test_access_control_edit_works(qtbot: QtBot):
    """Tests whether the access control checkboxes work. """
    view = QDialog()
    acl = GroupACL(group="biru-group1")
    project = Project(groups=[acl])
    tab = ProjectAccessControlTab(view)
    tab.set_data(project)
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    # Find the coordinate of the checkmark for is owner and click it.
    acl_table = tab.ui.groups.ui.aclTable
    is_owner_checkbox = acl_table.visualRect(acl_table.model().index(0,1)).center()
    viewport = acl_table.viewport()
    qtbot.mouseClick(viewport, Qt.MouseButton.LeftButton, pos=is_owner_checkbox)
    qtbot.wait(100)
    # New check the underlying access control property is changed.
    assert acl.is_owner is True