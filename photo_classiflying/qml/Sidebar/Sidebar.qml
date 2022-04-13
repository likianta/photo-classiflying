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
            bottom: _base_toolbar.top
            margins: 8
//             bottomMargin: 8
        }
        defaultWidth: root.defaultWidth
        expandedWidth: root.expandedWidth
        expanded: root.expanded
    }

    BaseToolbar {
        id: _base_toolbar
        anchors {
            left: parent.left
            bottom: parent.bottom
            margins: 8
        }
        width: root.defaultWidth - 8
        onExpandClicked: {
            root.expanded = !root.expanded
        }
        onNewItemClicked: {
            PySidebarModelForGroup3.qappend({
                'mark': '_',
                'count': 0,
                'title': '',
                'dirpath': '',
            })
        }
    }

    ExtendToolbar {
        id: _extend_toolbar
        visible: root.expanded
        anchors {
            left: _base_toolbar.right
            bottom: parent.bottom
            margins: 8
        }
        width: root.expandedWidth - root.defaultWidth
    }
}
