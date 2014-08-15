import QtQuick 2.0
import QtQuick.Controls 1.0
import QtQuick.Layouts 1.0

ApplicationWindow {
    id: root

    width: 500
    height: 300
    title: qsTr("hey")

    property string msg

    signal printMessage(string message)
    signal showMessage()

    Action {
        id: applicationQuit 
        shortcut: "Ctrl+Q"
        onTriggered: Qt.quit
    }

    GroupBox {
        anchors.centerIn: parent
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
        }
    }
}
