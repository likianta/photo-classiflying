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

    onFocusChanged: {
        if (!this.activeFocus) {
            this.submitted(this.text)
        }
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
        this.focus = false
        event.accepted = true
    }
    Keys.onTabPressed: (event) => {
        this.focus = false
        event.accepted = true
    }
    Keys.onBacktabPressed: (event) => {
        this.focus = false
        event.accepted = true
    }
}
