import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

ApplicationWindow {
    id: root

    width: 500
    height: 300
    title: qsTr("hey")

    property string msg
    // property ListElement pythonListModel

    signal printMessage(string message)
    signal showMessage()

    Keys.onEscapePressed: Qt.quit


    Action {
        id: applicationQuit 
        shortcut: "Ctrl+Q"
        onTriggered: Qt.quit
    }

    GroupBox {
        // anchors.centerIn: parent
        ColumnLayout {
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
                            text.text = root.msg
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

            ComboBox {
                currentIndex: 2
                model: ListModel {
                    id: cbItems
                    ListElement { text: "Banana"; color: "Yellow" }
                    ListElement { text: "Apple"; color: "Green" }
                    ListElement { text: "Coconut"; color: "Brown" }
                    ListElement { text: "Orange"; color: "Orange" }
                }
                width: 200
                onCurrentIndexChanged: console.debug(cbItems.get(currentIndex).text + ", " + cbItems.get(currentIndex).color)
            }

            TableView {
                // anchors.centerIn: parent
                // model: fruitModel
                TableViewColumn {role: "text"; title: "Column 1" }
                // height: 50
                // headerVisible: false
                model: pythonListModel
                // model: 20
            }
        }
    }
}
