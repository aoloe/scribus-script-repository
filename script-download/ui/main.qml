import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

ApplicationWindow {
    id: root

    width: 500
    height: 300
    title: qsTr("hey")

    property string msg
    onMsgChanged: {
        console.debug("test")
        text.text = msg // root.msg
    }

    signal printMessage(string message)
    signal showMessage()


    Action {
        id: applicationQuit 
        shortcut: "Ctrl+Q"
        onTriggered: Qt.quit
    }

    Rectangle {

        // Keys.onEscapePressed: Qt.quit

        // anchors.centerIn: parent
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
                    id: buttonsLayout
                    anchors.fill: parent
                    Button {
                        objectName: "printButton"
                        // anchors.centerIn: parent
                        text: "Print it"
                        onClicked: printMessage("abcd")
                    }

                    Button {
                        objectName: "getButton"
                        // anchors.centerIn: parent
                        text: "Get it"
                        onClicked: { // multiple actions
                            showMessage()
                            // text.text = root.msg
                            // text.text = "abc"
                        }
                    }

                    Button {
                        text: qsTr("Cancel")
                        onClicked: Qt.quit()
                        Keys.onEscapePressed: Qt.quit()
                        // Keys.onEscapePressed: Qt.quit()
                    }
                }
            } 
            ExclusiveGroup {
                id:group
            }

            GroupBox {
                ColumnLayout {
                    RadioButton {
                        text: "button 1"
                        exclusiveGroup: group
                    }
                    RadioButton {
                        text: "button 2"
                        exclusiveGroup: group
                    }
                    RadioButton {
                        text: "button 3"
                        exclusiveGroup: group
                    }
                }
            }

            TextField {
                id: "text"
                objectName: "text"
            }
        }
    }
}
