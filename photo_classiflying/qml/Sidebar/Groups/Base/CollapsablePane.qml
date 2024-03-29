import QtQuick

Item {
    clip: true
    width: expanded ? expandedWidth : defaultWidth

    property int  defaultWidth
    property int  expandedWidth
    property bool expanded

    property Item  listview: _listview
    property alias model: _listview.model
    property var   options: null

    ListView {
        id: _listview
        anchors.fill: parent
        delegate: GeneralItem {
            width: _listview.width
            height: 32
            defaultWidth: root.defaultWidth
            expandedWidth: root.expandedWidth
            expanded: root.expanded
            rootModel: _listview.model
            Component.onCompleted: {
                if (root.options) {
                    this.options = root.options
                }
            }
        }
    }
}
