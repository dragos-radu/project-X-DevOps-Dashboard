import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: root
    width: 1280
    height: 800
    visible: true
    color: "#020617"
    title: "PiOps Dashboard"

    DashboardScreen {
        anchors.fill: parent
    }
}