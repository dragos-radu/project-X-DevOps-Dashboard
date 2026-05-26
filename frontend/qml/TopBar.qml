import QtQuick
import QtQuick.Layouts

Rectangle {
    radius: 14
    color: "#071426"
    border.color: "#10233f"
    border.width: 1

    RowLayout {
        anchors.fill: parent
        anchors.margins: 22
        spacing: 34

        Text {
            text: Qt.formatTime(new Date(), "HH:mm")
            color: "white"
            font.pixelSize: 42
            font.bold: true
            Layout.fillWidth: true
        }

        TopMetric { label: "WiFi"; value: "Conns" }
        TopMetric { label: "Temp"; value: "48°C" }
        TopMetric { label: "RAM"; value: "42%" }
        TopMetric { label: "CPU"; value: "15%" }
    }
}