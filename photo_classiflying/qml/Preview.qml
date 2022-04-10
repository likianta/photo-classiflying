import QtQuick
import "./Common" as C

Item {
    id: root
    clip: true

    property string mark: '0'
    property alias  source: _img.source
    property int    __fillMode: 0
    property real   __ratio: width / height
    signal clicked()

    function switchFillMode() {
        if (root.__fillMode == 0) {
            root.__fillMode = 1
        } else {
            root.__fillMode = 0
        }
    }

    function resetFillMode() {
        root.__fillMode = 0
    }

    C.RoundedImage {
        id: _img

        function setFillMode(mode) {
            if (mode == 0) {
                if (
                    _img.sourceSize.width <= root.width &&
                    _img.sourceSize.height <= root.height
                ) {
                    _img.width = _img.sourceSize.width
                    _img.height = _img.sourceSize.height
                    _img.x = (root.width - _img.width) / 2
                    _img.y = (root.height - _img.height) / 2
                } else {
                    const ratio = _img.sourceSize.width / _img.sourceSize.height
                    if (ratio == root.__ratio) {
                        // assert _img.sourceSize.width > root.width and
                        //  _img.sourceSize.height > root.height
                        _img.width = root.width
                        _img.height = root.height
                        _img.x = 0
                        _img.y = 0
                    } else if (ratio > root.__ratio) {
                        // width > height
                        _img.width = root.width
                        _img.height = _img.width / ratio
                        _img.x = 0
                        _img.y = (root.height - _img.height) / 2
                    } else {
                        // height > width
                        _img.height = root.height
                        _img.width = _img.height * ratio
                        _img.x = (root.width - _img.width) / 2
                        _img.y = 0
                    }
                }
            } else {
                // fit the window width
                const ratio = _img.sourceSize.width / _img.sourceSize.height
                _img.width = root.width
                _img.height = _img.width / ratio
                _img.x = 0
                if (_img.height > root.height) {
                    _img.y = 0
                } else {
                    _img.y = (root.height - _img.height) / 2
                }
            }
//            console.log(
//                [root.width, root.height, mode],
//                [_img.sourceSize.width, _img.sourceSize.height],
//                [_img.width, _img.height, _img.x, _img.y]
//            )
        }

        onStatusChanged: {
            if (this.status == Image.Ready) {
                this.setFillMode(root.__fillMode)
            }
        }

//        Behavior {
//            animation: NumberAnimation {
//                target: targetProperty.object
//                properties: 'width, height, x, y'
//                duration: 100
//            }
//        }

//        Behavior on width {
//            NumberAnimation {
//                duration: 100
//            }
//        }
//
//        Behavior on height {
//            NumberAnimation {
//                duration: 100
//            }
//        }
//
//        Behavior on x {
//            NumberAnimation {
//                duration: 100
//            }
//        }
//
//        Behavior on y {
//            NumberAnimation {
//                duration: 100
//            }
//        }
    }

    MouseArea {
        anchors.fill: parent
        enabled: parent.__fillMode == 1 && _img.height > parent.height

        onClicked: {
            root.clicked()
        }

        onWheel: (wheel) => {
            const y = _img.y + wheel.angleDelta.y
//            console.log(_img.y, wheel.angleDelta.y, y)

            if (y > 0) {  // already at the top, cannot scroll up any more.
                _img.y = 0
            } else {  // assert y < 0
                const visiblePart = _img.height + y
                if (visiblePart < parent.height) {
                    // scroll to the bottom
                    _img.y = -(_img.height - parent.height)
                } else {
                    _img.y = y
                }
            }

            wheel.accepted = true
        }
    }

    C.ImageMask {
        anchors.fill: parent
        animDuration: 0
        masked: parent.mark != '0'
        style: 1
        text: parent.mark
    }

    Component.onCompleted: {
        console.log(this.width, this.height)
        this.__fillModeChanged.connect(() => {
            _img.setFillMode(this.__fillMode)
        })
//        PyMainProg.mark_updated.connect((mark) => this.mark = mark)
    }
}
