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
}
