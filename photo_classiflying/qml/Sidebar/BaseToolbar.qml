import QtQuick
import "../Common" as C

Row {
    id: root
    height: 32
    spacing: 4

    signal expandClicked()
    signal newItemClicked()

    C.Button {
        text: 'expand'
        anchors.bottom: parent.bottom
        onClicked: root.expandClicked()
    }

    C.Button {
        text: 'new item'
        anchors.bottom: parent.bottom
        onClicked: root.newItemClicked()
    }
}
