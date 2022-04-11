from os.path import exists

from lk_utils import dumps
from lk_utils import loads

from lk_qtquick_scaffold import Model
from lk_qtquick_scaffold import signal
from ..paths import sidebar_model as model_path


class PySidebarModel(Model):
    # # signal[int index, str mark, int count]
    # # _count_updated = signal(int, str, int)
    # _count_updated = signal(str, int)  # signal[str mark, int count]
    _count_updated = signal(int, int)  # signal[int index, int count]
    
    def __init__(self):
        super().__init__(role_names=('mark', 'count', 'title', 'dirpath'))
        self.path_2_mark = {}  # path means 'file path'
        self.mark_2_paths = {}
        self.mark_2_index = {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'a': 10,
            'b': 11,
            'c': 12,
            'd': 13,
            'e': 14,
            'f': 15,
            'g': 16,
            'h': 17,
            'i': 18,
            'j': 19,
            'k': 20,
            'l': 21,
            'm': 22,
            'n': 23,
            'o': 24,
            'p': 25,
            'q': 26,
            'r': 27,
            's': 28,
            't': 29,
            'u': 30,
            'v': 31,
            'w': 32,
            'x': 33,
            'y': 34,
            'z': 35,
        }
        self._count_updated.connect(
            lambda index, count: self.update(
                index=index, item={'count': count}
            )
        )
        
        # init model
        if not exists(model_path):
            from ..config import user_config
            self.mark_2_paths.update(
                {mark: set() for mark in self.mark_2_index}
            )
            entries = [
                {'mark': mark, 'count': 0, 'title': '', 'dirpath': ''}
                for mark in self.mark_2_index
            ]
            # load predefined paths
            # note: '0' (index=0) and 'z' (index=35) are reserved marks.
            # PERF: shall we sort the predefined paths?
            for i, p in enumerate(user_config['predefined_paths'], 1):
                if i >= 35: break
                entries[i]['dirpath'] = p
                entries[i]['title'] = p.rsplit('/', 1)[-1]
            self.append_many(entries)
            dumps({
                'path_2_mark' : self.path_2_mark,
                'mark_2_paths': self.mark_2_paths,
                'entries'     : entries,
            }, model_path)
        else:
            data = loads(model_path)
            self.path_2_mark = data['path_2_mark']
            self.mark_2_paths = data['mark_2_paths']
            self.append_many(data['entries'])
    
    def update_mark(self, mark: str, path: str):
        if path in self.path_2_mark:
            last_mark = self.path_2_mark[path]
            self.mark_2_paths[last_mark].remove(path)
            self._count_updated.emit(
                self.mark_2_index[last_mark],
                len(self.mark_2_paths[last_mark])
            )
        self.path_2_mark[path] = mark
        self.mark_2_paths[mark].add(path)
        self._count_updated.emit(
            self.mark_2_index[mark],
            len(self.mark_2_paths[mark])
        )
    
    def sort_marks(self):
        backup = self._items[1:-1]
        # print(':vl', backup)
        #   top and bottom don't participate in the sort.
        # sort by: tuple[bool is_empty, str text]
        #   is_empty: True first, False last
        # https://cloud.tencent.com/developer/ask/219983
        backup.sort(key=lambda x: (not bool(x['dirpath']), x['dirpath']))
        backup.sort(key=lambda x: (not bool(x['title']), x['title']))
        # print(':vl', backup)
        # rebuild marks in order.
        for item, mark in zip(
                [None] + backup + [None],
                self.mark_2_index.keys()
        ):
            if item is None: continue
            item['mark'] = mark
        self.update_many(1, 1 + len(backup), backup)
    
    def add_file(self, path: str, mark='0'):
        self.path_2_mark[path] = mark
        self.mark_2_paths[mark].add(path)
        self._count_updated.emit(
            self.mark_2_index[mark],
            len(self.mark_2_paths[mark])
        )
    
    def remove_file(self, path: str):
        mark = self.path_2_mark.pop(path)
        self.mark_2_paths[mark].remove(path)
        self._count_updated.emit(
            self.mark_2_index[mark],
            len(self.mark_2_paths[mark])
        )
    
    # noinspection PyMethodOverriding
    def clear(self, mark: str) -> tuple[str, ...]:
        out = tuple(self.mark_2_paths[mark])
        for path in self.mark_2_paths[mark]:
            self.path_2_mark.pop(path)
        self.mark_2_paths[mark].clear()
        self._count_updated.emit(self.mark_2_index[mark], 0)
        return out
    
    def save(self):
        dumps({
            'path_2_mark' : self.path_2_mark,
            'mark_2_paths': self.mark_2_paths,
            'entries'     : self.items
        }, model_path)
