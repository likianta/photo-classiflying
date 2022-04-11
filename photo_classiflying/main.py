import os
import shutil

from PySide6.QtCore import QObject
from lk_utils import currdir
from lk_utils import fs

from lk_qtquick_scaffold import app
from lk_qtquick_scaffold import hot_loader  # noqa
from lk_qtquick_scaffold import slot
from .keybindings import PyKeyBindings
from .model import PySidebarModel
from .model import PyThumbnailModel
from . import paths

os.chdir(currdir())


class PyMainProgram(QObject):
    
    def __init__(self, gallery_dir: str):
        super().__init__()
        
        self._current_thumb_index = 0
        self._recycler_dir = paths.recycle_bin
        
        self._thumbnail_model = PyThumbnailModel(gallery_dir)
        self._sidebar_model = PySidebarModel()
        self._key_bindings = PyKeyBindings()
        
        self._thumbnail_model.file_added.connect(
            self._sidebar_model.add_file)
        self._thumbnail_model.file_removed.connect(
            self._sidebar_model.remove_file)
        self._key_bindings.mark_updated.connect(self._update_mark)
        
        app.register_pyobj(self._thumbnail_model, 'PyThumbnailModel')
        app.register_pyobj(self._sidebar_model, 'PySidebarModel')
        app.register_pyobj(self._key_bindings, 'PyKeyBindings')
        app.register_pyobj(self, 'PyMainProg')
        
        app.on_exit.connect(self.close)
    
    def close(self):
        print('remember sidebar settings')
        self._sidebar_model.save()
        self._thumbnail_model.save()
    
    @slot(str, str)
    def move_group_items(self, mark: str, dirpath: str):
        if not dirpath or not os.path.isdir(dirpath):
            print('invalid folder', dirpath)
            return
        else:
            dirpath = fs.normpath(dirpath)
        
        paths = self._sidebar_model.clear(mark=mark)
        for p in paths:
            file_i = p
            file_o = dirpath + '/' + (name := os.path.basename(p))
            print('move', name, ':v2')
            shutil.move(file_i, file_o)
            self._thumbnail_model.remove_path(p)
    
    @slot()
    def recycle_group_items(self):
        paths = self._sidebar_model.clear(mark='z')
        for p in paths:
            file_i = p
            file_o = self._recycler_dir + '/' + (name := os.path.basename(p))
            print('recycle', name, ':v2')
            shutil.move(file_i, file_o)
            self._thumbnail_model.remove_path(p)
    
    @slot()
    def refresh_gallery(self):
        self._thumbnail_model.refresh_gallery()
    
    @slot(int)
    def set_current_thumb_index(self, index: int):
        self._current_thumb_index = index
    
    @slot()
    def sort_marks(self):
        self._sidebar_model.sort_marks()
    
    def _update_mark(self, mark: str):
        self._thumbnail_model.update(
            index=self._current_thumb_index,
            item={'mark': mark}
        )
        self._sidebar_model.update_mark(
            mark=mark,
            path=self._thumbnail_model[self._current_thumb_index]['filepath']
        )


_holder = []  # runtime holder, avoid python gc.


def main(gallery_dir: str):
    # from PySide6.QtQuickControls2 import QQuickStyle
    # QQuickStyle.setStyle('Imagine')
    _holder.append(PyMainProgram(gallery_dir))
    app.start('./qml/Main.qml')
    # hot_loader.start('./qml/Main.qml')
