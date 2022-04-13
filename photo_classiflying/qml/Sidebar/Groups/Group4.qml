import QtQuick
import "Base" as B

B.CollapsablePane {
    id: root
    height: 32 * 2 + 4 * 1

    model: PySidebarModelForGroup4
    options: {
        'group_index': 3,
        'show_index': false,
        'title': 'delete',
        'dynamic_title': false,
        'show_clear_button': false,
        'show_exec_button': true,
        'exec_button_name': 'move',
        'custom_exec_button_func': false,
    }

    Component.onCompleted: {
        let item

        item = root.listview.itemAtIndex(0)
        item.titleItem.text = 'finalized'
        item.dirpathItem.visible = false
        item.btn1.visible = false
        item.btn2.visible = false

        item = root.listview.itemAtIndex(1)
        item.titleItem.text = 'deleted'
        item.dirpathItem.visible = false
        //  PERF: make dirpathItem visible but not editable.
        item.btn1.visible = false
        item.btn2.text = 'delete'
    }
}
