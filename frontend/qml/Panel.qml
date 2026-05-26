import QtQuick
import QtQuick.Controls

Rectangle {
    id: panel

    property string title: ""

    radius: 14
    color: "#071426"
    border.color: "#10233f"
    border.width: 1
    clip: true

    Rectangle {
        id: titleBar

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top

        height: 34
        color: "#0A182B"   // ~2% lighter/different than #071426

        radius: panel.radius

        Rectangle {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: parent.radius
            color: parent.color
        }

        Text {
            text: panel.title

            anchors.left: parent.left
            anchors.leftMargin: 14
            anchors.verticalCenter: parent.verticalCenter

            color: "#E5E7EB"
            font.family: "Rajdhani"
            font.pixelSize: 14
            font.weight: Font.DemiBold
            font.letterSpacing: 0.5
        }
    }
}