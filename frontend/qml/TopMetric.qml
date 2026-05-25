import QtQuick

Column {
    spacing: 4

    Text {
        text: label
        color: "#9ca3af"
        font.pixelSize: 15
    }

    Text {
        text: value
        color: "#e5e7eb"
        font.pixelSize: 21
        font.bold: true
    }

    property string label: ""
    property string value: ""
}