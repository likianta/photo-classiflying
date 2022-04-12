import QtQuick

Rectangle {
    width: expanded ? expandedWidth : defaultWidth
    radius: 8
    clip: true
    color: '#041533'  // dark blue
    z: 1

    property int  defaultWidth: 200
    property int  expandedWidth: 400
    property bool expanded: false

    Behavior on width {
        NumberAnimation {
            duration: 100
        }
    }

    MouseArea {  // the MouseArea is just used to prevent mouse events
        //  pentration to underlay.
        anchors.fill: parent
        preventStealing: true
        propagateComposedEvents: false
    }
}
