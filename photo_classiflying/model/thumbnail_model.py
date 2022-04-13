import os.path
from datetime import datetime

from lk_utils import dumps
from lk_utils import fs
from lk_utils import loads

from lk_qtquick_scaffold import Model
from lk_qtquick_scaffold import signal
from ..paths import thumbnail_model as model_path


class PyThumbnailModel(Model):
    file_added = signal(str)
    file_removed = signal(str)
    
    def __init__(self, gallery_dir):
        super().__init__(role_names=(
            'filepath', 'filename', 'created', 'mark',
        ))
        self._gallery_root = gallery_dir
        self._paths = []
        if os.path.exists(model_path):
            db = loads(model_path)
            self.append_many(db['items'])
            self._paths.extend(db['paths'])
    
    def load_gallery(self) -> int:
        if self.items:
            # self.refresh_gallery()
            # return len(self.items)
            self.clear()
            self._paths.clear()
        
        print('loading gallery...')
        for fp, fn in fs.find_files(self._gallery_root):
            self.append({
                'filepath': fp,
                'filename': fn,
                'created' : _get_file_created_time(fp),
                'mark'    : '0',
            })
        print(self._gallery_root, len(self.items))
        return len(self.items)
    
    def refresh_gallery(self) -> tuple[int, int]:
        # return: tuple[int added, int removed]
        old_paths = set(self._paths.copy())
        new_paths = []
        for p in fs.find_file_paths(self._gallery_root):
            if p in old_paths:
                old_paths.remove(p)
            else:
                new_paths.append(p)
        if old_paths:  # there are some files not exists anymore.
            for p in old_paths:
                self.remove_path(p)
        if new_paths:
            self.append_many([
                {
                    'filepath': p,
                    'filename': os.path.basename(p),
                    'created' : _get_file_created_time(p),
                    'mark'    : '0',
                } for p in new_paths
            ])
        return len(new_paths), len(old_paths)
    
    def remove_path(self, path: str):
        index = self._paths.index(path)
        self.delete(index)
    
    # -------------------------------------------------------------------------
    # override
    
    def append(self, item):
        super().append(item)
        self._paths.append(item['filepath'])
        self.file_added.emit(item['filepath'])
    
    def append_many(self, items):
        super().append_many(items)
        for x in items:
            self._paths.append(x['filepath'])
            self.file_added.emit(x['filepath'])
    
    def delete(self, index):
        super().delete(index)
        path = self._paths.pop(index)
        self.file_removed.emit(path)
    
    def save(self):
        dumps({
            'items': self._items,
            'paths': self._paths,
        }, model_path)


def _get_file_created_time(file: str) -> str:
    # return format: `yyyymmdd-hhnnss`. e.g. `20220405-235524`
    return datetime.fromtimestamp(
        os.path.getctime(file)
    ).strftime('%Y%m%d-%H%M%S')
