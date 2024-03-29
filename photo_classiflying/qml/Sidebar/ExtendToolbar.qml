import QtQuick
import "../Common" as C

Row {
    height: 32
    spacing: 4

    C.Button {
        anchors.bottom: parent.bottom
        text: 'sort'
        onClicked: {
            PyMainProg.sort_marks()
        }
    }

    C.Button {
        anchors.bottom: parent.bottom
        text: 'refresh'
        onClicked: {
            PyMainProg.refresh_gallery()
        }
    }
}
