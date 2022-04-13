import QtQuick
import "./Common" as C

ListView {
    id: root
    height: 120
    cacheBuffer: 500  // additional rendered pixels outside visible area
    //  suggest not greater than the width of view. make it near to mouse
    //  scroll speed (or x2 faster).
    clip: true
    currentIndex: -1
    model: PyThumbnailModel
    orientation: ListView.Horizontal
    spacing: 4
    
    property Item preview
    signal clicked()

    function nextImage() {
        root.incrementCurrentIndex()
    }

    function prevImage() {
        root.decrementCurrentIndex()
    }

    onCurrentIndexChanged: {
        if (!this.currentItem) {
            // this may be happened when user exits the application.
            return
        }
        preview.source = this.currentItem.source
        preview.mark = Qt.binding(() => {
            if (this.currentItem) {
                return this.currentItem.mark
            } else {
                // this may be happened when user exits the application.
                return ''
            }
        })
//        preview.mark = this.currentItem.mark
        preview.resetFillMode()
        PyMainProg.set_current_thumb_index(this.currentIndex)
    }

    delegate: Rectangle {
        // the height is fixed, but width is dynamic
        width: height * _img.sourceSize.width / _img.sourceSize.height
        height: root.height
        radius: 4
//        border.width: 4
        border.width: model.index == root.currentIndex ? 4 : 2
        border.color: model.index == root.currentIndex ? 'blue' : '#cdcdcd'

        property string mark: model.mark
        property alias  source: _img.source

        C.RoundedImage {
            id: _img
            anchors {
                fill: parent
                margins: parent.border.width + 1
            }
            radius: parent.radius
            source: 'file:///' + model.filepath

            C.ImageMask {
                anchors.fill: parent
                fontSize: 24
                masked: parent.parent.mark != '0'
                style: 2
                text: parent.parent.mark
            }
        }
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                root.currentIndex = model.index
                root.clicked()
            }
        }
    }

    MouseArea {  // to support horizontal scroll
        anchors.fill: parent
        propagateComposedEvents: true
        onWheel: (wheel) => {
            root.flick(wheel.angleDelta.y * 10, 0)
            wheel.accepted = true
        }
    }

    Component.onCompleted: {
        this.model.load_gallery()
        this.currentIndex = 0
    }
}
