import QtQuick

// button in dark theme.
Rectangle {
    width: 0
    height: 24
    border.width: 1
    border.color: _area.containsMouse ? '#ffffff' : '#dddddd'
    color: _area.pressed ? '#bbbbbb' : '#1A2135'  // deep gray : gray
    radius: 8

    property alias font: _txt.font
    property alias isHovered: _area.containsMouse
    property alias text: _txt.text
    property alias textColor: _txt.color
    signal clicked()
    signal released()

    Text {
        id: _txt
        anchors.centerIn: parent
        color: 'white'
    }

    MouseArea {
        id: _area
        anchors.fill: parent
        hoverEnabled: true
        onClicked: parent.clicked()
        onReleased: parent.released()
    }

    Component.onCompleted: {
        if (this.width == 0) {
            this.width = _txt.contentWidth + 24
        }
    }
}
