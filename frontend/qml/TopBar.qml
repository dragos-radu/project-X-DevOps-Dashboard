import QtQuick
import QtQuick.Layouts
import "components"

Rectangle {
    radius: 14
    color: "#071426"
    border.color: "#10233f"
    border.width: 1

    Row {
        id: leftBranding

        anchors.left: parent.left
        anchors.leftMargin: 20
        anchors.verticalCenter: parent.verticalCenter

        spacing: 8

        Image {
            id: brandIcon

            source: "assets/continuous.png"
            width: 40
            height: 40
            fillMode: Image.PreserveAspectFit
            anchors.verticalCenter: parent.verticalCenter
            smooth: true
        }

        Column {
            anchors.verticalCenter: parent.verticalCenter
            spacing: 1

            Text {
                text: "Pi DevOps Command Center"
                color: "#E5E7EB"
                font.family: "Rajdhani"
                font.pixelSize: 16
                font.bold: true
                font.letterSpacing: 0.4
            }

            Text {
                text: "Monitor. Automate. Deliver."
                color: "#2a35c8"
                font.family: "Rajdhani"
                font.pixelSize: 12
                font.bold: true
                font.letterSpacing: 0.5
            }
        }
    }

    Column {
        id: dateTimeStack

        width: 140
        spacing: 1

        anchors.verticalCenter: parent.verticalCenter
        x: (parent.width * 5 / 11) - (width / 2)

        Text {
            id: timeText
            anchors.horizontalCenter: parent.horizontalCenter
            text: Qt.formatTime(new Date(), "HH:mm")
            color: "#F8F9FA"
            font.family: "Rajdhani"
            font.pixelSize: 26
            font.bold: true
            font.letterSpacing: 1.2
        }

        Text {
            id: dateText
            anchors.horizontalCenter: parent.horizontalCenter
            text: Qt.formatDate(new Date(), "dd MMM yyyy")
            color: "#F8F9FA"
            font.family: "Rajdhani"
            font.pixelSize: 12
            font.weight: Font.Medium
            font.letterSpacing: 0.6
        }

        Text {
            id: dayText
            anchors.horizontalCenter: parent.horizontalCenter
            text: Qt.formatDate(new Date(), "dddd")
            color: "#F8F9FA"
            font.family: "Rajdhani"
            font.pixelSize: 12
            font.weight: Font.Medium
            font.letterSpacing: 0.6
        }
    }

    Timer {
        interval: 1000
        running: true
        repeat: true

        onTriggered: {
            const now = new Date()
            timeText.text = Qt.formatTime(now, "HH:mm")
            dateText.text = Qt.formatDate(now, "dd MMMM yyyy")
            dayText.text = Qt.formatDate(now, "dddd")
        }
    }

    Row {
        id: rightInfoBoxes

        anchors.verticalCenter: parent.verticalCenter

        x: dateTimeStack.x + dateTimeStack.width + 50
        width: parent.width - x - 10
        height: parent.height * 0.75

        spacing: 0

        Repeater {
            model: 5

            Rectangle {
                property real widthRatio: {
                    if (index === 0) return 1.0      // Pi status
                    if (index === 1) return 1.35     // CPU
                    if (index === 2) return 1.35     // RAM
                    if (index === 3) return 0.65     // Temp
                    if (index === 4) return 0.65     // Signal
                    return 1.0
                }

                width: rightInfoBoxes.width * widthRatio / 5.0
                height: rightInfoBoxes.height
                color: "transparent"

                Rectangle {
                    width: 1
                    height: parent.height * 0.65
                    color: "#F8F9FA"
                    opacity: 0.7

                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                }

                Column {
                    visible: index === 0

                    anchors.left: parent.left
                    anchors.leftMargin: 5
                    anchors.verticalCenter: parent.verticalCenter

                    spacing: 4

                    Text {
                        anchors.left: parent.left
                        text: "Pi status"
                        color: "#FFFFFF"
                        font.pixelSize: 9
                        font.bold: true
                    }

                    Row {
                        anchors.left: parent.left
                        spacing: 4

                        Rectangle {
                            width: 7
                            height: 7
                            radius: 3.5
                            color: "#22C55E"
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        Text {
                            text: "Online"
                            color: "#22C55E"
                            font.pixelSize: 9
                            font.bold: true
                        }
                    }

                    Text {
                        anchors.left: parent.left
                        text: "Uptime: " + systemMetrics.uptime
                        color: "#FACC15"
                        font.pixelSize: 8
                    }
                }

                Rectangle {
                    visible: index === 4

                    width: 44
                    height: 34
                    radius: 10
                    color: "#0F172A"
                    anchors.centerIn: parent

                    Row {
                        anchors.centerIn: parent
                        spacing: 3

                        property int signalLevel: systemMetrics ? systemMetrics.wifiLevel : 0
                        property color activeColor: "#2a35c8"
                        property color inactiveColor: "#1E293B"

                        Rectangle {
                            width: 5
                            height: 10
                            radius: 2
                            anchors.bottom: parent.bottom
                            color: parent.signalLevel >= 1 ? parent.activeColor : parent.inactiveColor
                            opacity: parent.signalLevel >= 1 ? 1.0 : 0.5
                        }

                        Rectangle {
                            width: 5
                            height: 15
                            radius: 2
                            anchors.bottom: parent.bottom
                            color: parent.signalLevel >= 2 ? parent.activeColor : parent.inactiveColor
                            opacity: parent.signalLevel >= 2 ? 1.0 : 0.5
                        }

                        Rectangle {
                            width: 5
                            height: 20
                            radius: 2
                            anchors.bottom: parent.bottom
                            color: parent.signalLevel >= 3 ? parent.activeColor : parent.inactiveColor
                            opacity: parent.signalLevel >= 3 ? 1.0 : 0.5
                        }

                        Rectangle {
                            width: 5
                            height: 25
                            radius: 2
                            anchors.bottom: parent.bottom
                            color: parent.signalLevel >= 4 ? parent.activeColor : parent.inactiveColor
                            opacity: parent.signalLevel >= 4 ? 1.0 : 0.5
                        }
                    }
                }

                Row {
                    visible: index === 1

                    anchors.left: parent.left
                    anchors.leftMargin: 14
                    anchors.right: parent.right
                    anchors.rightMargin: 8
                    anchors.verticalCenter: parent.verticalCenter

                    height: parent.height * 0.75
                    spacing: 6

                    Column {
                        width: 30
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 3

                        Text {
                            text: "CPU"
                            color: "#FFFFFF"
                            font.pixelSize: 9
                            font.bold: true
                        }

                        Text {
                            text: systemMetrics.cpu
                            color: "#38BDF8"
                            font.pixelSize: 12
                            font.bold: true
                        }
                    }

                    MiniLineChart {
                        width: parent.width - 30 - parent.spacing
                        height: 30
                        anchors.verticalCenter: parent.verticalCenter
                        values: systemMetrics.cpuHistory
                        lineColor: "#a9aee1"
                        fillColor: "#2a35c8"
                    }
                }

                Row {
                    visible: index === 2

                    anchors.left: parent.left
                    anchors.leftMargin: 14
                    anchors.right: parent.right
                    anchors.rightMargin: 8
                    anchors.verticalCenter: parent.verticalCenter

                    height: parent.height * 0.75
                    spacing: 6

                    Column {
                        width: 30
                        anchors.verticalCenter: parent.verticalCenter
                        spacing: 3

                        Text {
                            text: "RAM"
                            color: "#FFFFFF"
                            font.pixelSize: 9
                            font.bold: true
                        }

                        Text {
                            text: systemMetrics.ram
                            color: "#A78BFA"
                            font.pixelSize: 12
                            font.bold: true
                        }
                    }

                    MiniLineChart {
                        width: parent.width - 30 - parent.spacing
                        height: 30
                        anchors.verticalCenter: parent.verticalCenter
                        values: systemMetrics.ramHistory
                        lineColor: "#a9aee1"
                        fillColor: "#2a35c8"
                    }
                }

                Rectangle {
                    visible: index === 3

                    width: parent.width * 0.9
                    height: 40
                    radius: 10
                    color: "#0F172A"

                    anchors.centerIn: parent

                    Row {
                        anchors.centerIn: parent

                        Image {
                            source: "assets/temperature.png"
                            width: 25
                            height: 25
                            fillMode: Image.PreserveAspectFit
                            anchors.verticalCenter: parent.verticalCenter
                            opacity: 0.9
                        }

                        Text {
                            text: systemMetrics.temperature
                            color: "#FACC15"
                            font.pixelSize: 11
                            font.bold: true
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }
            }
        }
    }
}