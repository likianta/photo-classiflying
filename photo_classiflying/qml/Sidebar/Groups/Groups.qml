import QtQuick

Column {
    id: root
    spacing: 4

    property int  defaultWidth
    property int  expandedWidth
    property bool expanded

    component Spacer: Rectangle {
        width: root.defaultWidth
        height: 1
        color: '#888888'
    }

    Group1 {
        id: _group1
        height: 32
        defaultWidth: root.defaultWidth
        expandedWidth: root.expandedWidth
        expanded: root.expanded
    }

    Spacer {}

    Group2 {
        id: _group2
        height: 200
        defaultWidth: root.defaultWidth
        expandedWidth: root.expandedWidth
        expanded: root.expanded
    }

    Spacer {}

    Group3 {
        id: _group3
        height: 240
        defaultWidth: root.defaultWidth
        expandedWidth: root.expandedWidth
        expanded: root.expanded
    }

    Spacer {}

    Group4 {
        id: _group4
        height: 64
        defaultWidth: root.defaultWidth
        expandedWidth: root.expandedWidth
        expanded: root.expanded
    }
}
