import QtQuick

Item {
    // docs: see `photo_quick_sort.keybindings.py : PyKeyBindings.handle_key`
    property Item preview
    property Item thumbnails

    Keys.onPressed: (event) => {
        PyKeyBindings.handle_key(
            event.key, event.text,
            event.modifiers & Qt.ShiftModifier
        )
    }

    Component.onCompleted: {
        PyKeyBindings.init(preview, thumbnails)
    }
}
