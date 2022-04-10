import QtQuick
import "../Common" as C

BasePane {
    id: root
    clip: true

    signal editingFinished(string title)
    signal selected(int index)

    ListView {
        id: _listview
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
            bottom: _expand_btn.top
            margins: 12
        }
        clip: true
        model: PySidebarModel
        spacing: 4

        delegate: Item {
            id: _item
//            width: _listview.width
            width: root.expandedWidth
            height: 32

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    root.selected(model.index)
                }
            }

            Row {
                anchors.fill: parent
                clip: true
                spacing: 4

                Text {
                    id: _mark
                    anchors.verticalCenter: parent.verticalCenter
                    color: 'white'
                    font.bold: true
                    font.family: 'Sarasa Term SC'
                    font.pixelSize: 12
                    text: model.mark
                }

                Text {
                    id: _count
                    anchors.verticalCenter: parent.verticalCenter
                    color: '#888888'
        //            font.family: 'Sarasa Term SC'
                    font.pixelSize: 12
                    text: '(' + model.count + ')'
                }

                C.TextEdit {
                    id: _title
                    anchors.verticalCenter: parent.verticalCenter
                    width: root.defaultWidth - 12 - x - 12
//                    clip: true
                    text: model.title
                    onSubmitted: (text) => {
                        const result = PySidebarModel.qupdate(
                            model.index, {'title': text}
                        )
                        console.log(model.index, JSON.stringify(result))
                        root.editingFinished(text)
                    }
                }

                Text {
                    // just a spacer
                    anchors.verticalCenter: parent.verticalCenter
                    color: '#666666'
                    text: '|'
                }

                C.TextEdit {
                    id: _dirpath
                    visible: root.expanded && (
                        model.mark != '0' || model.mark != 'z'
                    )
                    anchors.verticalCenter: parent.verticalCenter
                    width: root.expandedWidth - 12
                        - _expand_btn.width - 4
                        - x - 12
                    text: model.dirpath

                    onSubmitted: (text) => {
                        PySidebarModel.qupdate(
                            model.index, {'dirpath': text}
                        )
                        root.editingFinished(this.text)
                    }

                    onTextChanged: {
                        const autoTitle = pyside.eval(`
                            dirpath = dirpath.replace('\\\\', '/')
                            if '/' in dirpath:
                                return dirpath.rsplit('/', 1)[1]
                            else:
                                return ''
                        `, {'dirpath': this.text})
                        if (autoTitle) {
                            _title.text = autoTitle
                        }
                    }
                }

                C.Button {
                    id: _exec_btn
                    visible: root.expanded
                    anchors.verticalCenter: parent.verticalCenter
                    text: 'move'
                    Component.onCompleted: {
//                        console.log(model.index, model.mark)
                        switch (model.mark) {
                            case '0':
                                this.enabled = false
                                break
                            case 'z':
                                this.text = 'delete'
                                this.clicked.connect(() => {
                                    PyMainProg.recycle_group_items()
                                })
                                break
                            default:
                                this.clicked.connect(() => {
                                    PyMainProg.move_group_items(
                                        model.mark, _dirpath.text
                                    )
                                })
                                break
                        }
                    }
                }
            }
        }
    }

    C.Button {
        id: _expand_btn
        anchors {
//            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
            margins: 8
        }
        x: (root.defaultWidth - width) / 2
        text: 'expand'
        onClicked: {
            root.expanded = !root.expanded
        }
    }

    ExtendBar {
        visible: root.expanded
        anchors {
            bottom: parent.bottom
            margins: 8
        }
        x: root.defaultWidth + 12
        width: root.extendWidth - 12 - x
    }
}
