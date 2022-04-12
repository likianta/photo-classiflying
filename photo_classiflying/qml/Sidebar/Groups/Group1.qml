import QtQuick
import "Base" as B

B.CollapsablePane {
    id: root
    height: 32
    model: PySidebarModelForGroup1
    options: {
        'group_index': 0,
        'show_index': false,
        'title': 'root',
        'dynamic_title': false,
        'show_clear_button': false,
        'show_exec_button': false,
        'exec_button_name': 'move',
        'custom_exec_button_func': false,
    }
}
