import os

from PySide6.QtCore import QObject
from lk_utils import currdir

from lk_qtquick_scaffold import app
from lk_qtquick_scaffold import hot_loader  # noqa
from lk_qtquick_scaffold import slot
from . import paths
from .keybindings import PyKeyBindings
from .model import PyThumbnailModel
from .model import get_sidebar_models

os.chdir(currdir())


class PyMainProgram(QObject):
    
    def __init__(self, gallery_dir: str):
        super().__init__()
        
        self._current_thumb_index = 0
        self._recycler_dir = paths.recycle_bin
        
        self._thumbnail_model = PyThumbnailModel(gallery_dir)
        self._sidebar_models = get_sidebar_models(gallery_dir)
        self._key_bindings = PyKeyBindings()
        
        self._thumbnail_model.file_added.connect(
            self._sidebar_models[0].add_file)
        self._thumbnail_model.file_removed.connect(
            self._sidebar_models[0].remove_file)
        self._key_bindings.mark_updated.connect(
            self._update_mark)
        self._sidebar_models[2].mark_updated.connect(
            self._sidebar_models[1].update_mark)
        self._sidebar_models[2].resorted.connect(
            self._sidebar_models[1].resort_marks)
        
        app.register_pyobj(self._thumbnail_model, 'PyThumbnailModel')
        app.register_pyobj(self._sidebar_models[0], 'PySidebarModelForGroup1')
        app.register_pyobj(self._sidebar_models[1], 'PySidebarModelForGroup2')
        app.register_pyobj(self._sidebar_models[2], 'PySidebarModelForGroup3')
        app.register_pyobj(self._sidebar_models[3], 'PySidebarModelForGroup4')
        app.register_pyobj(self._key_bindings, 'PyKeyBindings')
        app.register_pyobj(self, 'PyMainProg')
        
        app.on_exit.connect(self.close)
    
    def close(self):
        print(':v2', 'saving application status')
        from .model import save_sidebar_models
        save_sidebar_models(self._sidebar_models)
        self._thumbnail_model.save()
    
    @slot(str, int)
    def move_paths(self, mark: str, model_index: int):
        paths = self._sidebar_models[model_index].move_paths(mark)
        for p in paths:
            self._thumbnail_model.remove_path(p)
    
    @slot()
    def refresh_gallery(self):
        self._thumbnail_model.refresh_gallery()
    
    @slot(int)
    def set_current_thumb_index(self, index: int):
        self._current_thumb_index = index
    
    @slot()
    def sort_marks(self):
        self._sidebar_models[2].sort_marks()
    
    def _update_mark(self, mark: str):
        from .model.index import mark_2_modelx, path_2_mark
        
        self._thumbnail_model.update(
            index=self._current_thumb_index,
            item={'mark': mark}
        )
        
        path = self._thumbnail_model[self._current_thumb_index]['filepath']
        if path in path_2_mark:
            old_mark, new_mark = path_2_mark[path], mark
            if old_mark == new_mark:
                return
        else:
            old_mark, new_mark = None, mark
        
        def get_method(model, model_index: int, inc: bool):
            """ get method of updating mark and count.
            
            args:
                inc: True: increase; False: decrease.
            """
            from functools import partial
            nonlocal mark, path
            
            method = model.increase_mark_count if inc \
                else model.decrease_mark_count
            
            # noinspection PyCompatibility
            match model_index:
                case 1:
                    raise Exception(
                        'the case is not impossible. it should be triggered by '
                        '`sidebar_models[2]` internally.'
                    )
                case _:
                    return partial(method, path=path)
        
        # ---------------------------------------------------------------------
        # 1. if mark in `path_2_uid`, call remove method.
        # 2. then call add method.
        
        if old_mark is not None:
            old_model_index = mark_2_modelx(old_mark)
            model = self._sidebar_models[old_model_index]
            method = get_method(model, old_model_index, False)
            method(old_mark)
        
        path_2_mark[path] = mark
        model_index = mark_2_modelx(mark)
        model = self._sidebar_models[model_index]
        method = get_method(model, model_index, True)
        method(mark)


_holder = []  # runtime holder, avoid python gc.


def main(gallery_dir: str):
    # from PySide6.QtQuickControls2 import QQuickStyle
    # QQuickStyle.setStyle('Imagine')
    _holder.append(PyMainProgram(gallery_dir))
    app.start('./qml/Main.qml')
    # hot_loader.start('./qml/Main.qml')
