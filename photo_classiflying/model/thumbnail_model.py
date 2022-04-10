import os.path
from datetime import datetime

from lk_utils import dumps
from lk_utils import fs
from lk_utils import loads
from lk_utils import relpath

from lk_qtquick_scaffold import Model
from lk_qtquick_scaffold import signal
from lk_qtquick_scaffold import slot

db_path = relpath('../../database/thumbnail_model.pkl')


class PyThumbnailModel(Model):
    file_added = signal(str)
    file_removed = signal(str)
    
    def __init__(self):
        super().__init__(role_names=(
            'filepath', 'filename', 'created', 'mark',
        ))
        self._gallery_root = 'C:/Likianta/test/2022-04/todo'  # TEST
        self._paths = []
        if os.path.exists(db_path):
            db = loads(db_path)
            self.append_many(db['items'])
            self._paths.extend(db['paths'])
    
    @slot(result=int)
    def load_gallery(self) -> int:
        if self._items:
            self.refresh_gallery()
            return len(self._items)
        
        self.clear()
        for fp, fn in fs.find_files(self._gallery_root):
            self.append({
                'filepath': fp,
                'filename': fn,
                'created' : _get_file_created_time(fp),
                'mark'    : '0',
            })
        print(self._gallery_root, len(self._items))
        return len(self._items)
    
    def refresh_gallery(self):
        paths = {
            x['filepath']: i for i, x in enumerate(self.items)
        }
        new_paths = []
        for p in fs.findall_file_paths(self._gallery_root):
            if p in paths:
                paths.pop(p)
            else:
                new_paths.append(p)
        # print(':l', paths, len(paths))
        # print(':l', new_paths, len(new_paths))
        if paths:  # there are some files deleted
            for p, i in paths.items():
                self.delete(i)
        if new_paths:
            self.append_many([
                {
                    'filepath': p,
                    'filename': os.path.basename(p),
                    'created' : _get_file_created_time(p),
                    'mark'    : '0',
                } for p in new_paths
            ])
    
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
        }, db_path)


def _get_file_created_time(file: str) -> str:
    # return format: `yyyymmdd-hhnnss`. e.g. `20220405-235524`
    return datetime.fromtimestamp(
        os.path.getctime(file)
    ).strftime('%Y%m%d-%H%M%S')
