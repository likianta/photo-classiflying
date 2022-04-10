from PySide6.QtCore import QObject
from PySide6.QtCore import Qt

from lk_qtquick_scaffold import signal
from lk_qtquick_scaffold import slot


class PyKeyBindings(QObject):
    mark_updated = signal(str)  # signal[str mark]
    last_mark: str = '0'
    
    _preview_item: QObject
    _thumbnails_item: QObject
    
    @slot(QObject, QObject)
    def init(self, preview_item, thumbnails_item):
        self._preview_item = preview_item
        self._thumbnails_item = thumbnails_item
        print(':v', 'bound with preview and thumbnails items')

    # noinspection PyUnusedLocal
    @slot(int, str, bool)
    def handle_key(self, code: int, key: str, shift: bool):
        """
        keys:
            control keys:
                - backtick/tilde: toggle preview image fill mode (fit/fill)
                - space/tab/right/down/page_down: next image
                - shift+space/shift+tab/left/up/page_up: previous image
                - enter: mark with last key and go to next image
                - esc: clear mark
            mark keys:
                - 0-9: mark with number
                - a-z: mark with letter
        """
        # if key:
        #     print(hex(code), key, shift)
        
        # ---------------------------------------------------------------------
        # mark keys
        mark_keys = {
            Qt.Key_0: '0',
            Qt.Key_1: '1',
            Qt.Key_2: '2',
            Qt.Key_3: '3',
            Qt.Key_4: '4',
            Qt.Key_5: '5',
            Qt.Key_6: '6',
            Qt.Key_7: '7',
            Qt.Key_8: '8',
            Qt.Key_9: '9',
            Qt.Key_A: 'a',
            Qt.Key_B: 'b',
            Qt.Key_C: 'c',
            Qt.Key_D: 'd',
            Qt.Key_E: 'e',
            Qt.Key_F: 'f',
            Qt.Key_G: 'g',
            Qt.Key_H: 'h',
            Qt.Key_I: 'i',
            Qt.Key_J: 'j',
            Qt.Key_K: 'k',
            Qt.Key_L: 'l',
            Qt.Key_M: 'm',
            Qt.Key_N: 'n',
            Qt.Key_O: 'o',
            Qt.Key_P: 'p',
            Qt.Key_Q: 'q',
            Qt.Key_R: 'r',
            Qt.Key_S: 's',
            Qt.Key_T: 't',
            Qt.Key_U: 'u',
            Qt.Key_V: 'v',
            Qt.Key_W: 'w',
            Qt.Key_X: 'x',
            Qt.Key_Y: 'y',
            Qt.Key_Z: 'z',
        }
        
        # mark and goto next image
        if code in mark_keys:
            mark = mark_keys[code]
            self.mark_updated.emit(mark)
            self.last_mark = mark
            self._thumbnails_item.nextImage()
        
        # ---------------------------------------------------------------------
        # control keys
        
        # switch fill mode
        elif code in (
                Qt.Key_QuoteLeft, Qt.Key_AsciiTilde
        ):
            self._preview_item.switchFillMode()
        
        # next image
        elif not shift and code in (
                Qt.Key_Space, Qt.Key_Tab, Qt.Key_Right, Qt.Key_Down,
                Qt.Key_PageDown
        ):
            self._thumbnails_item.nextImage()
        
        # prev image
        elif shift and code in (
                Qt.Key_Space, Qt.Key_Tab
        ):
            self._thumbnails_item.prevImage()
        elif code in (
                Qt.Key_Backtab,
        ):
            self._thumbnails_item.prevImage()
        elif code in (
                Qt.Key_Left, Qt.Key_Up, Qt.Key_PageUp
        ):
            self._thumbnails_item.prevImage()
        
        # mark uses last and goto next image
        elif code in (
                Qt.Key_Enter, Qt.Key_Return
        ):
            self.mark_updated.emit(self.last_mark)
            self._thumbnails_item.nextImage()
        
        # reset mark but not goto next image
        elif code == Qt.Key_Escape:
            self.mark_updated.emit('0')
            self.last_mark = '0'
