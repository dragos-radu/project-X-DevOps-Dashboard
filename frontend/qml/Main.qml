import QtQuick
import QtQuick.Controls

ApplicationWindow {
    id: root
    width: 1024
    height: 600
    visible: true
    color: "#020617"
    title: "PiOps Dashboard"
    visibility: Window.FullScreen

    // Remove the system title bar and borders
    flags: Qt.FramelessWindowHint

    font.family: "DejaVu Sans"

    DashboardScreen {
        anchors.fill: parent
    }
}