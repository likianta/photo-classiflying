import QtQuick
import "Base" as B

B.CollapsablePane {
    id: root
    height: 32 * 9 + 4 * 8

    model: PySidebarModelForGroup2
    options: {
        'group_index': 1,
        'show_index': true,
        'title': '',
        'dynamic_title': false,
        'show_clear_button': false,
        'show_exec_button': false,
        'exec_button_name': 'move',
        'custom_exec_button_func': false,
    }
}
