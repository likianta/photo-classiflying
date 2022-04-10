import QtQuick
import "../Common" as C

C.TextEdit {
    Keys.onReturnPressed: (event) => {
        if (this.text) {
            root.newItemCreated(this.text)
        }
    }
}
//Row {
//    id: root
//    height: 32
//    spacing: 4
//
//    signal newItemCreated(string title)
//
//    Rectangle {
//        anchors.verticalCenter: parent.verticalCenter
//        width: 24
//        height: 24
//        radius: 4
//        color: '#dddddd'
//
//        property bool listenToKeyBind: false
//
//        Text {
//            id: _mark
//            anchors.centerIn: parent
//            color: 'white'
//            font.pixelSize: 12
//        }
//
//        MouseArea {
//            anchors.fill: parent
//            onClicked: {
//                parent.listenToKeyBind = !parent.listenToKeyBind
//            }
//        }
//
//        Keys {
//            enabled: parent.listenToKeyBind
//            onPressed: (event) => {
//                const mark = PyKeyBindings.handle_binding_mark(event.key)
//                _mark.text = mark
//                parent.listenToKeyBind = false
//            }
//        }
//    }
//
//    C.TextEdit {
//        anchors.verticalCenter: parent.verticalCenter
//        width: parent.width - x - 12
//        text: ''
//
//        Keys.onReturnPressed: (event) => {
//            if (this.text) {
//                root.newItemCreated(this.text)
//            }
//        }
//    }
//}
