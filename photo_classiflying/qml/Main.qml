import QtQuick
import QtQuick.Controls
import "Sidebar"

Window {
    id: root
    visible: true
    width: __width_1 + __width_2
    height: 640

    property int __width_1: 180
    property int __width_2: 720

    function setDefaultFocus() {
        _keybindings.forceActiveFocus()
    }

    MouseArea {
        // click the spare space to set focus on default object.
        anchors.fill: parent
        onClicked: root.setDefaultFocus()
    }

    Sidebar {
        id: _sidebar
        anchors {
            left: parent.left
            top: parent.top
            bottom: parent.bottom
            margins: 8
        }
        defaultWidth: root.__width_1
        expandedWidth: root.__width_1 + 400
        onEditingFinished: {
            root.setDefaultFocus()
        }
    }

    Preview {
        id: _preview
        anchors {
            left: parent.left
            leftMargin: root.__width_1 + 12
            right: parent.right
            top: parent.top
            bottom: _thumbnails.top
            margins: 8
        }
        onClicked: {
            root.setDefaultFocus()
        }
    }

    Thumbnails {
        id: _thumbnails
        anchors {
            left: parent.left
            leftMargin: root.__width_1 + 12
            right: parent.right
            bottom: parent.bottom
            margins: 8
        }
        height: 120
        preview: _preview
        onClicked: {
            root.setDefaultFocus()
        }
    }

    Button {
        id: _test_btn
        visible: false
        anchors {
            right: parent.right
            bottom: parent.bottom
            margins: 8
        }
        text: 'test something'
        onClicked: {
            console.log(_preview.source, _thumbnails.count)
        }
    }

    KeyBindings {
        id: _keybindings
        thumbnails: _thumbnails
        preview: _preview
    }

    Component.onCompleted: {
        root.setDefaultFocus()
    }
}
