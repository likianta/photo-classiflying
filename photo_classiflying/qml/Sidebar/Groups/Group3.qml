import QtQuick
import "Base" as B

B.CollapsablePane {
    id: root
    height: 32 * 26 + 4 * 25

    model: PySidebarModelForGroup3
    options: {
        'group_index': 2,
        'show_index': false,
        'title': '',
        'dynamic_title': true,
        'show_clear_button': true,
        'show_exec_button': true,
        'exec_button_name': 'move',
        'custom_exec_button_func': false,
    }
}
