import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: root

    Rectangle {
        anchors.fill: parent
        color: "#020617"
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        TopBar {
            id: topBar
            Layout.fillWidth: true
            Layout.preferredHeight: root.height * 0.13
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 10

            Panel {
                title: "DevOps News"
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 5
            }

            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 3
                spacing: 10

                Panel {
                    title: "CI/CD Pipelines"
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredHeight: 4
                }

                Panel {
                    title: "System Status"
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredHeight: 3

                    SystemStatusContent {
                        anchors.fill: parent
                    }
                }
            }

            ColumnLayout {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.preferredWidth: 3
                spacing: 10

                Panel {
                    title: "Notifications"
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredHeight: 4
                }

                Panel {
                    title: "Services"
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredHeight: 3
                }
            }
        }

        BottomBar {
            Layout.fillWidth: true
            Layout.preferredHeight: root.height * 0.0975
        }
    }
}