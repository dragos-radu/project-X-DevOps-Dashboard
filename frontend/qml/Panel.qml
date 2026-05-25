import QtQuick
import QtQuick.Controls

Rectangle {
    id: panel

    property string title: ""

    radius: 14
    color: "#071426"
    border.color: "#10233f"
    border.width: 1

    Text {
        text: panel.title
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.margins: 18
        color: "#e5e7eb"
        font.pixelSize: 22
        font.bold: true
    }
}