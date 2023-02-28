from typing import List
from PyQt5.QtCore import QModelIndex, QUrl, Qt
from PyQt5.QtWidgets import QDataWidgetMapper, QDialog, QHeaderView, QLabel, QLineEdit, QListView, QTableView, QVBoxLayout, QWidget
from pytestqt.qtbot import QtBot
import pytest
from ime.models import Experiment, IngestionMetadata
from ime.widgets.access_control_tab import AccessControlTab
from PyQt5.QtQuick import QQuickView

@pytest.fixture
def experiments():
    # This path is relative to where pytest is run.
    # So run pytest at the root directory.
    with open('ime/tests/fixtures_access_control_tab.yaml') as f:
        content = f.read()
        fixtures = IngestionMetadata.from_yaml(content)
        return fixtures.experiments


def test_show_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    view = QDialog()
    experiment = experiments[0]
    tab = AccessControlTab(view)
    tab.data = experiment
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    qtbot.stop()

def test_edit_access_control_tab(qtbot: QtBot, experiments: List[Experiment]):
    view = QDialog()
    experiment = experiments[0]
    tab = AccessControlTab(view)
    tab.data = experiment
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    model = tab.ui.readGroupsList._model
    edit_location = model.index(0,0)
    assert model.data(edit_location, Qt.ItemDataRole.DisplayRole) == "ghil983"
    edit_location = model.index(0,0)
    model.setData(edit_location,"Testing editing")
    qtbot.stop()
    assert experiment.read_groups is not None
    assert experiment.read_groups[0] == "Testing editing"

def test_tab_with_inheritance(qtbot: QtBot, experiments: List[Experiment]):
    view = QDialog()
    experiment = experiments[0]
    tab = AccessControlTab(view)
    tab.data = experiment
    qtbot.add_widget(view)
    view.show()
    qtbot.wait_exposed(view)
    assert tab.ui.adminGroupsList.ui.aclList.isEnabled()

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
