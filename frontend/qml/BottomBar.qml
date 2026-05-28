import QtQuick
import QtQuick.Layouts
import "components"
import "utils/WeatherIconMapper.js" as WeatherIconMapper

Rectangle {
    property int weatherCode: weatherController ? weatherController.weatherCode : -1

    radius: 14
    color: "#071426"
    border.color: "#10233f"
    border.width: 1

    RowLayout {
        anchors.fill: parent
        anchors.leftMargin: 14
        anchors.rightMargin: 10
        anchors.topMargin: 8
        anchors.bottomMargin: 8
        spacing: 18

        Item {
            id: weatherCluster

            Layout.fillWidth: true
            Layout.preferredWidth: 600
            Layout.minimumWidth: 560
            Layout.fillHeight: true

            Row {
                id: weatherRow

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                spacing: 12

                Rectangle {
                    width: 38
                    height: 38
                    radius: 10
                    color: "#0F172A"
                    border.color: "#1E293B"
                    border.width: 1
                    anchors.verticalCenter: parent.verticalCenter

                    Rectangle {
                        visible: weatherIcon.status !== Image.Ready
                        width: 18
                        height: 18
                        radius: 9
                        color: "#38BDF8"
                        opacity: 0.18
                        anchors.centerIn: parent

                        Rectangle {
                            width: 8
                            height: 8
                            radius: 4
                            color: "#94A3B8"
                            opacity: 0.55
                            anchors.centerIn: parent
                        }
                    }

                    Image {
                        id: weatherIcon

                        source: weatherController && weatherController.iconPath ? weatherController.iconPath : WeatherIconMapper.iconForCode(weatherCode)
                        visible: status === Image.Ready
                        width: 32
                        height: 32
                        fillMode: Image.PreserveAspectFit
                        smooth: true
                        anchors.centerIn: parent
                    }
                }

                Column {
                    width: 72
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 0

                    Text {
                        text: weatherController ? weatherController.temperature : "--°"
                        color: "#F8F9FA"
                        font.family: "Rajdhani"
                        font.pixelSize: 24
                        font.bold: true
                    }

                    Text {
                        text: weatherController ? weatherController.status : "Loading"
                        color: "#94A3B8"
                        font.family: "Rajdhani"
                        font.pixelSize: 12
                        font.weight: Font.Medium
                        elide: Text.ElideRight
                        width: parent.width
                    }
                }

                Column {
                    width: 112
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 2

                    Text {
                        text: weatherController ? weatherController.minMax : "--° / --°"
                        color: "#CBD5E1"
                        font.family: "Rajdhani"
                        font.pixelSize: 15
                        font.bold: true
                    }

                    Text {
                        text: weatherController ? weatherController.location : "Colibași, Giurgiu"
                        color: "#94A3B8"
                        font.family: "Rajdhani"
                        font.pixelSize: 11
                        elide: Text.ElideRight
                        width: parent.width
                    }
                }

                Rectangle {
                    width: 1
                    height: 28
                    color: "#1E293B"
                    anchors.verticalCenter: parent.verticalCenter
                }

                Item {
                    width: Math.max(220, weatherCluster.width - 271)
                    height: weatherCluster.height
                    anchors.verticalCenter: parent.verticalCenter

                    Row {
                        anchors.centerIn: parent
                        spacing: 8

                        Text {
                            text: sunPathIndicator.leftTimeText
                            color: "#94A3B8"
                            font.family: "Rajdhani"
                            font.pixelSize: 12
                            font.bold: true
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        SunPathIndicator {
                            id: sunPathIndicator

                            width: 128
                            height: 30
                            sunriseTime: weatherController ? weatherController.sunrise : "--:--"
                            sunsetTime: weatherController ? weatherController.sunset : "--:--"
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        Text {
                            text: sunPathIndicator.rightTimeText
                            color: "#94A3B8"
                            font.family: "Rajdhani"
                            font.pixelSize: 12
                            font.bold: true
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }
            }
        }

        Rectangle {
            Layout.preferredWidth: 1
            Layout.preferredHeight: 34
            Layout.alignment: Qt.AlignVCenter
            color: "#1E293B"
        }

        Item {
            Layout.fillWidth: true
            Layout.preferredWidth: 210
            Layout.minimumWidth: 150
            Layout.fillHeight: true

            Column {
                width: Math.min(parent.width, 190)
                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                spacing: 1

                Text {
                    text: calendarController ? calendarController.firstEventName : "Loading calendar"
                    color: "#F8F9FA"
                    font.family: "Rajdhani"
                    font.pixelSize: 17
                    font.bold: true
                    elide: Text.ElideRight
                    width: parent.width
                }

                Text {
                    text: calendarController ? calendarController.firstEventDateTime : ""
                    color: "#94A3B8"
                    font.family: "Rajdhani"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.preferredWidth: 220
            Layout.minimumWidth: 170
            Layout.fillHeight: true

            Column {
                width: Math.min(parent.width, 200)
                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                spacing: 1

                Text {
                    text: calendarController && calendarController.secondEventName ? "Next: " + calendarController.secondEventName : "Next: --"
                    color: "#CBD5E1"
                    font.family: "Rajdhani"
                    font.pixelSize: 15
                    font.bold: true
                    horizontalAlignment: Text.AlignRight
                    elide: Text.ElideRight
                    width: parent.width
                }

                Text {
                    text: calendarController ? calendarController.secondEventDateTime : ""
                    color: "#94A3B8"
                    font.family: "Rajdhani"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    horizontalAlignment: Text.AlignRight
                    width: parent.width
                }
            }
        }
    }
}
