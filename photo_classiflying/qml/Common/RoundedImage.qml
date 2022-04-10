import QtQuick
import Qt5Compat.GraphicalEffects

Image {
    id: root

    property int radius: 4

    layer.enabled: true
    layer.effect: OpacityMask {
        maskSource: Rectangle {
            width: root.width
            height: root.height
            radius: root.radius
        }
    }
}
