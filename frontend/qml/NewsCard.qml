import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    property string title: ""
    property string subtitle: ""
    property string status: ""

    Layout.fillWidth: true
    Layout.fillHeight: true
    radius: 22
    color: "#111827"
    border.color: "#1f2937"
    border.width: 1

    Column {
        anchors.fill: parent
        anchors.margins: 22
        spacing: 12

        Text {
            text: title
            color: "white"
            font.pixelSize: 26
            font.bold: true
        }

        Text {
            text: subtitle
            color: "#9ca3af"
            font.pixelSize: 16
            wrapMode: Text.WordWrap
            width: parent.width
        }

        Rectangle {
            width: statusText.width + 22
            height: 34
            radius: 17
            color: "#064e3b"

            Text {
                id: statusText
                anchors.centerIn: parent
                text: status
                color: "#a7f3d0"
                font.pixelSize: 14
                font.bold: true
            }
        }
    }
}