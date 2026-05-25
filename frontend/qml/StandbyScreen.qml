import QtQuick
import QtQuick.Controls

Item {
    id: root
    signal openDashboard()

    Rectangle {
        anchors.fill: parent
        color: "black"
    }

    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: {
            clockText.text = Qt.formatTime(new Date(), "HH:mm")
            dateText.text = Qt.formatDate(new Date(), "dddd, dd MMMM")
        }
    }

    Column {
        anchors.centerIn: parent
        spacing: 10

        Text {
            id: clockText
            text: Qt.formatTime(new Date(), "HH:mm")
            color: "white"
            font.pixelSize: 96
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
        }

        Text {
            id: dateText
            text: Qt.formatDate(new Date(), "dddd, dd MMMM")
            color: "#9ca3af"
            font.pixelSize: 24
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: "tap to open PiOps"
            color: "#4b5563"
            font.pixelSize: 16
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: root.openDashboard()
    }
}