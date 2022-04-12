import QtQuick
import "Groups"
import "../Common" as C

BasePane {
    id: root
    clip: true

    signal editingFinished(string title)
    signal selected(int index)

    Groups {
        id: _listview
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            bottom: _expand_btn.top
            margins: 8
//             bottomMargin: 8
        }
        defaultWidth: root.defaultWidth
        expandedWidth: root.expandedWidth
        expanded: root.expanded
    }

    C.Button {
        id: _expand_btn
        anchors {
//            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
            margins: 8
        }
        x: (root.defaultWidth - width) / 2
        text: 'expand'
        onClicked: {
            root.expanded = !root.expanded
        }
    }

    ExtendBar {
        visible: root.expanded
        anchors {
            bottom: parent.bottom
            margins: 8
            leftMargin: 0
        }
        x: root.defaultWidth
        width: root.expandedWidth - x
    }
}
