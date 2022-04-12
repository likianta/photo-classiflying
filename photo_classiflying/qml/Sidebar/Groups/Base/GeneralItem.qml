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
//     property var  model
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

    signal execClicked()

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
        width: root.defaultWidth - x
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

    B.Text {
        // just a spacer
        visible: root.expanded
        anchors.verticalCenter: parent.verticalCenter
        text: '|'
    }

    C.TextEdit {
        id: _dirpath
        visible: root.expanded
        anchors.verticalCenter: parent.verticalCenter
        width: 240
        text: model.dirpath
    }

    C.Button {
        id: _clear_btn
        visible: root.expanded && root.options['show_clear_button']
        anchors.verticalCenter: parent.verticalCenter
        text: 'clear'
        onClicked: {
            // FIXME: `_dirpath.text = ...` will break the binding mechanism
            //  between text and model. we have to make a workaround to
            //  reconnect them.
            _dirpath.text = ''
            _dirpath.submitted('')
            // this is the workaround.
            _dirpath.text = Qt.binding(() => model.dirpath)
        }
    }
    
    C.Button {
        id: _exec_btn
        visible: root.expanded && root.options['show_exec_button']
        anchors.verticalCenter: parent.verticalCenter
        text: root.options['exec_button_name']
        Component.onCompleted: {
            if (root.options['custom_exec_button_func']) {
                this.clicked.connect(root.execClicked)
            } else {
                this.clicked.connect(() => {
                    PyMainProg.move_paths(
                        model.mark,
                        root.options['group_index'],
                    )
                })
            }
        }
    }
}
