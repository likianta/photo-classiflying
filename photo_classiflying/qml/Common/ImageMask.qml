import QtQuick

Item {
    id: root

    property int   animDuration: 100
    property alias fontSize: _text.font.pixelSize
    property bool  masked: false
    property int   style: 0
    //  0: show full mask and centered text.
    //  1: show circle background for centered text.
    //  2: show full mask and addtional circle background for centered text.
    property alias text: _text.text

    Rectangle {
        id: _full_mask
        visible: parent.style != 1
        anchors.fill: parent
        color: 'black'
        opacity: parent.masked ? 0.5 : 0

        Behavior on opacity {
            enabled: root.animDuration > 0
            NumberAnimation {
                duration: root.animDuration
            }
        }
    }

    Rectangle {
        visible: parent.style != 0
        anchors.centerIn: parent
        width: _text.font.pixelSize * 1.8
        height: width
        radius: width / 2
        color: 'black'
        opacity: parent.masked ? 0.6 : 0

        Behavior on opacity {
            enabled: root.animDuration > 0
            NumberAnimation {
                duration: root.animDuration
            }
        }
    }

    Text {
        id: _text
        visible: parent.masked && _full_mask.opacity == 0.5
        anchors.centerIn: parent
        color: 'white'
//        font.bold: true
        font.pixelSize: 36
    }
}
