import QtQuick

Rectangle {
    id: card

    property string source: ""
    property string title: ""
    property string summary: ""
    property string publishedAt: ""

    width: parent ? parent.width : 420
    height: Math.max(88, contentColumn.implicitHeight + 20)
    radius: 10
    color: "#0B1A2E"
    border.color: "#1E293B"
    border.width: 1

    Column {
        id: contentColumn

        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 10
        spacing: 3

        Row {
            width: parent.width
            height: Math.max(sourceText.implicitHeight, timeText.implicitHeight)

            Text {
                id: sourceText

                width: parent.width - timeText.width - 10
                text: card.source
                color: "#38BDF8"
                font.family: "Rajdhani"
                font.pixelSize: 11
                font.bold: true
                elide: Text.ElideRight
            }

            Text {
                id: timeText

                text: card.publishedAt
                color: "#64748B"
                font.family: "Rajdhani"
                font.pixelSize: 10
                horizontalAlignment: Text.AlignRight
                x: parent.width - width
            }
        }

        Text {
            text: card.title
            color: "#F8F9FA"
            font.family: "Rajdhani"
            font.pixelSize: 15
            font.bold: true
            elide: Text.ElideRight
            width: parent.width
        }

        Text {
            text: card.summary || "No summary available"
            color: "#94A3B8"
            font.family: "Rajdhani"
            font.pixelSize: 11
            lineHeight: 0.92
            maximumLineCount: 2
            elide: Text.ElideRight
            wrapMode: Text.WordWrap
            width: parent.width
        }
    }
}
