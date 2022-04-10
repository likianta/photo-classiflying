import QtQuick

TextEdit {
    id: root
    clip: true
    color: '#888888'  // '#888888', 'white'
    font.pixelSize: 12
    selectByMouse: true

    property string underlineColor: '#666666'
    signal submitted(string text)

    onEditingFinished: {
        this.submitted(this.text)
    }

    Rectangle {
        anchors {
            left: parent.left
            right: parent.right
            bottom: parent.bottom
            bottomMargin: -1
        }
        color: root.underlineColor
        height: 1
    }

    Keys.onReturnPressed: (event) => {
        root.submitted(root.text)
        event.accepted = true
    }
    Keys.onTabPressed: (event) => {
        root.submitted(root.text)
        event.accepted = true
    }
    Keys.onBacktabPressed: (event) => {
        root.submitted(root.text)
        event.accepted = true
    }
}
