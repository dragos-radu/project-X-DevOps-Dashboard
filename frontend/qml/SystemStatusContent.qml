import QtQuick
import "components"

Item {
    id: root

    property int titleBarHeight: 34
    property real cpuValue: systemMetrics ? systemMetrics.cpuValue : 0
    property real ramValue: systemMetrics ? systemMetrics.ramValue : 0
    property real diskValue: systemMetrics ? systemMetrics.diskValue : 0

    property string hostnameValue: localSystemInfo ? localSystemInfo.hostname : "Unknown"
    property string osValue: localSystemInfo ? localSystemInfo.osName : "Unknown"
    property string localIpValue: localSystemInfo ? localSystemInfo.localIp : "Unavailable"

    Rectangle {
        id: horizontalLine

        x: 20
        y: titleBarHeight + ((parent.height - titleBarHeight) * 2 / 5)

        width: parent.width - 40
        height: 1

        color: "#FFFFFF"
        opacity: 0.7
    }

    Row {
        id: pieChartRow

        anchors.horizontalCenter: parent.horizontalCenter

        y: titleBarHeight + 2
        height: horizontalLine.y - y - 4

        spacing: 15

        PieMetric {
            width: 54
            height: 54

            label: "CPU"
            value: root.cpuValue
            valueText: Math.round(root.cpuValue) + "%"
            activeColor: "#38BDF8"
            trackColor: "#132B4A"
        }

        PieMetric {
            width: 54
            height: 54

            label: "RAM"
            value: root.ramValue
            valueText: Math.round(root.ramValue) + "%"
            activeColor: "#A78BFA"
            trackColor: "#132B4A"
        }

        PieMetric {
            width: 54
            height: 54

            label: "DISK"
            value: root.diskValue
            valueText: Math.round(root.diskValue) + "%"
            activeColor: "#FACC15"
            trackColor: "#132B4A"
        }
    }

    Column {
        id: systemInfoBlock

        anchors.top: horizontalLine.bottom
        anchors.topMargin: 10
        anchors.left: parent.left
        anchors.leftMargin: 20
        anchors.right: parent.right
        anchors.rightMargin: 20

        spacing: 7

        Item {
            width: parent.width
            height: 14

            Text {
                text: "Hostname"
                color: "#94A3B8"
                font.family: "Rajdhani"
                font.pixelSize: 10
                font.bold: true

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                text: root.hostnameValue
                color: "#F8F9FA"
                font.family: "Rajdhani"
                font.pixelSize: 11
                font.bold: true

                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        Item {
            width: parent.width
            height: 14

            Text {
                text: "OS"
                color: "#94A3B8"
                font.family: "Rajdhani"
                font.pixelSize: 10
                font.bold: true

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                text: root.osValue
                color: "#F8F9FA"
                font.family: "Rajdhani"
                font.pixelSize: 11
                font.bold: true

                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        Item {
            width: parent.width
            height: 14

            Text {
                text: "Local IP"
                color: "#94A3B8"
                font.family: "Rajdhani"
                font.pixelSize: 10
                font.bold: true

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                text: root.localIpValue
                color: "#F8F9FA"
                font.family: "Rajdhani"
                font.pixelSize: 11
                font.bold: true

                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}