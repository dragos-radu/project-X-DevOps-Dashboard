import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"

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

                Item {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 12
                    anchors.rightMargin: 12
                    anchors.topMargin: 46
                    anchors.bottomMargin: 12

                    Text {
                        anchors.centerIn: parent
                        visible: newsController.loading
                        text: "Loading news..."
                        color: "#94A3B8"
                        font.family: "Rajdhani"
                        font.pixelSize: 16
                        font.bold: true
                    }

                    Text {
                        anchors.centerIn: parent
                        visible: !newsController.loading && !newsController.online
                        text: "News unavailable"
                        color: "#94A3B8"
                        font.family: "Rajdhani"
                        font.pixelSize: 16
                        font.bold: true
                    }

                    Text {
                        anchors.centerIn: parent
                        visible: !newsController.loading && newsController.online && newsController.empty
                        text: "No news available"
                        color: "#94A3B8"
                        font.family: "Rajdhani"
                        font.pixelSize: 16
                        font.bold: true
                    }

                    ScrollView {
                        anchors.fill: parent
                        visible: !newsController.loading && newsController.online && !newsController.empty
                        clip: true

                        ListView {
                            width: parent.width
                            spacing: 8
                            model: newsController.items

                            delegate: NewsNotificationCard {
                                width: ListView.view.width
                                source: modelData.source
                                title: modelData.title
                                summary: modelData.summary
                                publishedAt: modelData.publishedAt
                            }
                        }
                    }
                }
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
