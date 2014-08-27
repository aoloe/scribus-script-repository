import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

ApplicationWindow {
    id: root

    width: 500
    height: 300
    title: qsTr("hey")

    Rectangle {
        focus: true
        Keys.onEscapePressed: Qt.quit()
        Keys.priority: Keys.BeforeItem
        ColumnLayout {
            GroupBox {
                RowLayout {
                    TextField {
                        width:100
                        id: "repositoryUrl"
                        objectName: "repositoryUrl"
                    }
                    ComboBox {
                        // currentIndex: 2
                        objectName: "repositoryType"
                        model: pythonRepositoryTypeModel
                        // onCurrentIndexChanged: console.debug(cbItems.get(currentIndex).text + ", " + cbItems.get(currentIndex).color)
                    }
                    Button {
                        objectName: "repositoryAdd"
                        text: "Add"
                    }
                }
            }
            ComboBox {
                // currentIndex: 2
                model: pythonRepositoryListModel
                // width: 200
                // onCurrentIndexChanged: console.debug(cbItems.get(currentIndex).text + ", " + cbItems.get(currentIndex).color)
            }
            TableView {
                TableViewColumn {
                    role: "scriptName"
                    title: "Column 1"
                }
                TableViewColumn {
                    role: "installed"
                    title: "Column 2"
                }
                headerVisible: false
                model: pythonScriptListModel
            }
            Text {
                text: "Script description"
            }
            GroupBox {
                RowLayout {
                    Button {
                        objectName: "scriptAdd"
                        text: "Add"
                    }
                }
            }
            GroupBox {
                RowLayout {
                    Button {
                        objectName: "scriptAdd"
                        text: "Run"
                    }
                    Button {
                        objectName: "scriptAdd"
                        text: "Remove"
                    }
                }
            }
            GroupBox {
                RowLayout {
                    Button {
                        text: qsTr("Cancel")
                        onClicked: Qt.quit()
                        Keys.onEscapePressed: Qt.quit()
                    }
                }
            } 
        }
    }
}
