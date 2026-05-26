import QtQuick

Item {
    id: root

    property string label: "CPU"
    property string valueText: "24%"
    property real value: 24

    property color activeColor: "#38BDF8"
    property color trackColor: "#132B4A"
    property color textColor: "#F8F9FA"
    property color labelColor: "#94A3B8"

    width: 54
    height: 54

    Canvas {
        id: canvas

        anchors.fill: parent

        onPaint: {
            const ctx = getContext("2d")
            ctx.clearRect(0, 0, width, height)

            const centerX = width / 2
            const centerY = height / 2
            const radius = Math.min(width, height) / 2 - 4
            const lineWidth = 3

            const startAngle = -Math.PI / 2
            const endAngle = startAngle + (Math.max(0, Math.min(100, root.value)) / 100) * Math.PI * 2

            // Track
            ctx.beginPath()
            ctx.arc(centerX, centerY, radius, 0, Math.PI * 2, false)
            ctx.strokeStyle = root.trackColor
            ctx.lineWidth = lineWidth
            ctx.lineCap = "butt"
            ctx.stroke()

            // Active arc
            ctx.beginPath()
            ctx.arc(centerX, centerY, radius, startAngle, endAngle, false)
            ctx.strokeStyle = root.activeColor
            ctx.lineWidth = lineWidth
            ctx.lineCap = "butt"
            ctx.stroke()
        }

        Connections {
            target: root

            function onValueChanged() {
                canvas.requestPaint()
            }

            function onActiveColorChanged() {
                canvas.requestPaint()
            }

            function onTrackColorChanged() {
                canvas.requestPaint()
            }
        }
    }

    Column {
        anchors.centerIn: parent
        spacing: -1

        Text {
            text: root.valueText
            color: root.textColor
            font.family: "Rajdhani"
            font.pixelSize: 10
            font.bold: true
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: root.label
            color: root.labelColor
            font.family: "Rajdhani"
            font.pixelSize: 6
            font.bold: true
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}