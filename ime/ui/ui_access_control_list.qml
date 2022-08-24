import QtQuick 2.4
import QtQuick.Controls 2.4

ScrollView {
    width: 200; height: 200

    Component {
        id: contactDelegate
        ItemDelegate {
            width: 180; height: 40
            text: '<b>Name:</b> ' + display
        }
    }

    ListView {
        model: listModel
        anchors.fill: parent
        delegate: contactDelegate
        highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
        focus: true
    }
}
