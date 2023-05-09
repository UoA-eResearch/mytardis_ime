from typing import List
from PyQt5.QtCore import QModelIndex, QUrl, Qt
from PyQt5.QtWidgets import QDataWidgetMapper, QDialog, QHeaderView, QLabel, QLineEdit, QListView, QTableView, QVBoxLayout, QWidget
from pytestqt.qtbot import QtBot
import pytest
from ime.models import Experiment, IngestionMetadata, Project
from ime.widgets.access_control_list import AccessControlList
from ime.widgets.access_control_tab import AccessControlTab
from PyQt5.QtQuick import QQuickView

@pytest.fixture
def metadata():
    # This path is relative to where pytest is run.
    # So run pytest at the root directory.
    with open('ime/tests/fixtures_access_control_tab.yaml') as f:
        content = f.read()
        return IngestionMetadata.from_yaml(content)


@pytest.fixture
def experiments(metadata: IngestionMetadata):
    return metadata.experiments

@pytest.fixture
def projects(metadata: IngestionMetadata):
    return metadata.projects


def test_show_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    """Tests access control tab can be created."""
    view = QDialog()
    experiment = experiments[0]
    tab = AccessControlTab(view)
    tab.set_data(experiment)
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)

def test_edit_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    """Test for editing an access control field results in changes in underlying model."""
    view = QDialog()
    experiment = experiments[0]
    tab = AccessControlTab(view)
    tab.set_data(experiment)
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    model = tab.ui.readGroupsList._model
    edit_location = model.index(0,0)
    assert model.data(edit_location, Qt.ItemDataRole.DisplayRole) == "ghil983"
    edit_location = model.index(0,0)
    model.setData(edit_location,"Testing editing")
    assert experiment.read_groups is not None
    assert experiment.read_groups[0] == "Testing editing"

def test_tab_with_inheritance(qtbot: QtBot, experiments: List[Experiment]):
    """Test for displaying a experiment's access control properly."""
    view = QDialog()
    experiment = experiments[0]
    tab = AccessControlTab(view)
    tab.set_data(experiment)
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    assert tab.ui.adminGroupsList.ui.aclList.isEnabled()

def test_tab_no_inheritance(qtbot: QtBot, projects: List[Project]):
    """Test for displaying a project's access control properly."""
    view = QDialog()
    project = projects[0]
    tab = AccessControlTab(view)
    tab.set_data(project)
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    for key in tab.views_by_field:
        # Go through each view, and check the override inherited checkbox isn't there,
        # and aclList can be edited/selected
        list_view = tab.views_by_field[key]
        assert not list_view.ui.overrideCheckBox.isVisible()
        assert list_view.ui.aclList.isEnabled()

def test_display_access_control_list(qtbot: QtBot, projects: List[Project]):
    view = QDialog()
    project = projects[0]
    aclist = AccessControlList(view)
    view.show()
    qtbot.wait_exposed(view)
    qtbot.stop()

# def disabled_test_qml_embed(qtbot: QtBot, experiments: List[Experiment]):
#     list_model = ListModel(experiments[0].admin_groups)
#     view = QQuickView()
#     context = view.rootContext()
#     context.setContextProperty("listModel", list_model)
#     widget = QWidget()
#     layout = QVBoxLayout(widget)
#     container = QWidget.createWindowContainer(view)
#     container.setFocusPolicy(Qt.FocusPolicy.TabFocus)
#     view.setSource(QUrl("ime/widgets/ui_access_control_list.qml"))
#     layout.addWidget(container)
#     qtbot.add_widget(widget)
#     container.setMinimumSize(200,200)
#     widget.show()
#     qtbot.wait_exposed(widget)
