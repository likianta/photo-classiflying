import QtQuick

Text {
    height: 32
//     horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter
    color: 'white'
    font.family: monospaced ? 'Sarasa Mono SC' : 'Microsoft YaHei UI'
    font.pixelSize: 12
    property bool monospaced: false
}
