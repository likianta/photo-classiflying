import QtQuick
import "./" as B
import "../../../Common" as C

Row {
    id: root
    height: 32
    spacing: 4

    property int  defaultWidth
    property int  expandedWidth
    property bool expanded
    property var  listviewModel: null  // optional
    property var  rootModel

    property var  options: {
        'group_index': -1,
        'show_index': false,
        'title': '',
        'dynamic_title': true,
//         'dirpath_readonly': false,
        'show_clear_button': true,
        'show_exec_button': true,
        'exec_button_name': 'move',
        'custom_exec_button_func': false,
    }

    // exposed properties
    property var btn1: _clear_btn
    property var btn2: _exec_btn
    property var dirpathItem: _dirpath
    property var titleItem: _title

    B.Text {
        visible: root.options['show_index']
        anchors.verticalCenter: parent.verticalCenter
        monospaced: true
        text: model.index + 1
    }

    B.Text {
        id: _mark
        anchors.verticalCenter: parent.verticalCenter
        monospaced: true
        text: model.mark
    }

    B.Text {
        id: _count
        anchors.verticalCenter: parent.verticalCenter
        color: '#888888'
        monospaced: true
        text: '(' + model.count + ')'
    }

    B.Text {
        id: _title
        width: root.defaultWidth - x - 4
        clip: true
        text: model.title
        Component.onCompleted: {
            if (root.options['title']) {
                this.text = root.options['title']
            } else if (root.options['dynamic_title']) {
                _dirpath.textChanged.connect(() => {
                    _title.text = pyside.eval(`
                        if not dirpath: return ''
                        dirpath = dirpath.replace('\\\\', '/')
                        if '/' in dirpath:
                            return dirpath.rsplit('/', 1)[1]
                        else:
                            return ''
                    `, {'dirpath': _dirpath.text})
                })
            }
        }
    }

//     B.Text {
//         // just a spacer
//         visible: root.expanded
//         anchors.verticalCenter: parent.verticalCenter
//         color: '#888888'
//         text: '|'
//     }

    C.TextEdit {
        id: _dirpath
        visible: root.expanded
        anchors.verticalCenter: parent.verticalCenter
        width: 240
        text: model.dirpath
        onSubmitted: (text) => {
            if (text == '') {
                root.rootModel.qupdate(
                    model.index, {'dirpath': '', 'title': ''}
                )
            } else {
                root.rootModel.qupdate(
                    model.index, {'dirpath': text, 'title': _title.text}
                )
            }
        }
    }

    C.Button {
        id: _clear_btn
        visible: root.expanded && root.options['show_clear_button']
        anchors.verticalCenter: parent.verticalCenter
        text: 'clear'
        onClicked: {
            _dirpath.submitted('')
        }
    }
    
    C.Button {
        id: _exec_btn
        visible: root.expanded && root.options['show_exec_button']
        anchors.verticalCenter: parent.verticalCenter
        text: root.options['exec_button_name']
        onClicked: {
            PyMainProg.move_paths(
                model.mark,
                root.options['group_index'],
            )
        }
    }
}
