import QtQuick
import QtQuick.Layouts

Rectangle {
    radius: 14
    color: "#071426"
    border.color: "#10233f"
    border.width: 1

    RowLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 42

        Text {
            text: "🍓 Raspberry Pi 5"
            color: "#e5e7eb"
            font.pixelSize: 20
            Layout.fillWidth: true
        }

        Text {
            text: "☁ 18°C  Partly Cloudy"
            color: "#cbd5e1"
            font.pixelSize: 18
            Layout.fillWidth: true
        }

        Text {
            text: "📅 DevOps Standup  Today 11:00"
            color: "#cbd5e1"
            font.pixelSize: 18
            Layout.fillWidth: true
        }

        Text {
            text: "📝 Notes"
            color: "#cbd5e1"
            font.pixelSize: 18
            Layout.fillWidth: true
        }
    }
}