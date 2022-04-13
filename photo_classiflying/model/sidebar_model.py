from uuid import uuid1

from lk_qtquick_scaffold import Model
from lk_qtquick_scaffold import signal
from lk_qtquick_scaffold import slot
from .index import *


class BaseModel(Model):
    MARK_2_INDEX: dict[str, int]
    model_index: int  # 0, 1, 2, 3
    uid_2_index: dict[str, int]
    
    def __init__(self, mark_2_index: dict[str, int]):
        super().__init__(role_names=(
            'uid', 'mark', 'count', 'title', 'dirpath'
        ))
        self.MARK_2_INDEX = mark_2_index
        self.uid_2_index = uid_2_index[self.model_index]
        for mark, index in mark_2_index.items():
            uid = str(uuid1())
            uid_2_paths[uid] = set()
            self.uid_2_index[uid] = index
            mark_2_uid[mark] = uid
            self.append({
                'uid'    : uid,
                'mark'   : mark,
                'count'  : 0,
                'title'  : '',
                'dirpath': '',
            })
    
    def restore_from_local(self, items: list[dict], ):
        self.clear()
        self.append_many(items)
    
    def increase_mark_count(self, mark: str, path: str):
        uid = mark_2_uid[mark]
        uid_2_paths[uid].add(path)
        
        index = self.uid_2_index[uid]
        self.update(index, {'count': len(uid_2_paths[uid])})
    
    def decrease_mark_count(self, mark: str, path: str):
        uid = mark_2_uid[mark]
        uid_2_paths[uid].remove(path)
        assert len(uid_2_paths[uid]) >= 0
        
        index = self.uid_2_index[uid]
        self.update(index, {'count': len(uid_2_paths[uid])})
    
    def move_paths(self, mark: str) -> tuple[str]:
        from os.path import basename
        from shutil import move
        
        uid = mark_2_uid[mark]
        index = self.uid_2_index[uid]
        dir_o = self.get(index)['dirpath']
        paths = tuple(uid_2_paths[uid])
        for p in paths:
            file_i = p
            file_o = '{}/{}'.format(dir_o, name := basename(p))
            print(':v2', 'move', name)
            move(file_i, file_o)
        
        uid_2_paths[uid].clear()
        for p in paths:
            path_2_mark.pop(p)
        self.update(index, {'count': 0})
        
        return paths
    
    def mark_2_index(self, mark: str) -> int:
        return self.uid_2_index[mark_2_uid[mark]]
    
    # -------------------------------------------------------------------------
    # override
    
    @slot(dict)
    def qappend(self, item: dict):
        new_uid = str(uuid1())
        new_idx = len(self._items)
        uid_2_paths[new_uid] = set()
        self.uid_2_index[new_uid] = new_idx
        super().append(item)
    
    def clear(self):
        for uid in self.uid_2_index.keys():
            paths = uid_2_paths.pop(uid)
            for p in paths:
                path_2_mark.pop(p)
            # mark `mark_2_uid` is invalid.
        self.uid_2_index.clear()
        super().clear()


class Model1(BaseModel):
    """ gallery root. """
    model_index = 0
    
    def __init__(self, gallery_dir: str):
        super().__init__(mark_2_index={'0': 0})
        # self._gallery_dir = gallery_dir
        self.update(0, {'title': 'default', 'dirpath': gallery_dir})
    
    @property
    def mark(self):
        return '0'
    
    @property
    def uid(self):
        return mark_2_uid['0']
    
    def init_paths(self, paths):
        uid_2_paths[self.uid] = set(paths)
        self.update(0, {'count': len(paths)})
    
    def add_file(self, path: str):
        uid_2_paths[self.uid].add(path)
        path_2_mark[path] = self.mark
        self.update(0, {'count': len(uid_2_paths[self.uid])})
    
    # noinspection PyUnusedLocal
    def remove_file(self, path: str):
        # note: `remove_file` is triggered when `Model4.move_paths` processed.
        # be noticed that `Model4.move_paths` has popped path from
        # `path_2_mark`. so we don't need to pop it here again.
        # # uid_2_paths[self.uid].remove(path)
        # # path_2_mark.pop(path)
        # assert len(uid_2_paths[self.uid]) >= 0
        #   actually, this assertion should be equal to ZERO.
        self.update(0, {'count': len(uid_2_paths[self.uid])})


class Model2(Model):
    """ recently used items.
    
    warning: `Model2` is inherited from `Model`, not `BaseModel`!
    
    differ with `BaseModel`:
        no uid.
        no mark, just nine blank items (placeholders).
        this model is passively triggered by `Model3`.
    """
    model_index = 1
    
    def __init__(self):
        super().__init__(role_names=(
            'uid', 'mark', 'count', 'title', 'dirpath'
        ))
        self.recent_marks = []
        self.append_many(
            [{'uid': '', 'mark': '', 'count': 0, 'title': '', 'dirpath': ''}]
            for _ in range(9)
        )
    
    def restore_from_local(self, items: list):
        assert len(items) == 9  # 1-9
        self.recent_marks = [x['mark'] for x in items]
        self.update_many(0, len(items), items)
    
    def update_mark(self, mark: str, count: int, title: str, dirpath: str):
        if mark in self.recent_marks:
            index = self.recent_marks.index(mark)
            self.update(index, {
                'count'  : count,
                'title'  : title,
                'dirpath': dirpath
            })
            return
        
        if len(self.recent_marks) == 9:
            self.recent_marks.pop()
            self.pop()
        
        self.recent_marks.insert(0, mark)
        self.insert(0, {
            'mark'   : mark,
            'count'  : count,
            'title'  : title,
            'dirpath': dirpath
        })
    
    def resort_marks(self, model3: 'Model3'):
        """
        this method is connected with `Model3.resorted` signal.
        """
        for i, item in enumerate(self.items):
            uid = item['uid']
            if not uid: continue
            model3_index = model3.uid_2_index[uid]
            model3_item = model3.get(model3_index)
            self.update(i, model3_item)


class Model3(BaseModel):
    """ all items. """
    model_index = 2
    is_dirty_sort: bool = False  # sort flag. see also `self.sort_marks`.
    
    mark_updated = signal(str, int, str, str)  # mark, count, title, dirpath
    resorted = signal(object)
    
    def __init__(self):
        super().__init__(
            mark_2_index={str(x): i for i, x in enumerate((
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            ))}
        )
        
        from os.path import basename
        from ..config import user_config
        predefined_paths = user_config['predefined_paths']
        for i, p in enumerate(predefined_paths):
            self.update(i, {'title': basename(p), 'dirpath': p})
    
    # noinspection PyMethodOverriding
    def restore_from_local(self, items: list[dict], is_dirty_sort: bool):
        super().restore_from_local(items)
        self.is_dirty_sort = is_dirty_sort
    
    def increase_mark_count(self, mark: str, path: str):
        super().increase_mark_count(mark, path)
        item = self.get(index=self.mark_2_index(mark))
        self.mark_updated.emit(
            mark, item['count'], item['title'], item['dirpath']
        )
    
    def decrease_mark_count(self, mark: str, path: str):
        super().decrease_mark_count(mark, path)
        item = self.get(index=self.mark_2_index(mark))
        self.mark_updated.emit(
            mark, item['count'], item['title'], item['dirpath']
        )
    
    def sort_marks(self):
        """
        workflow:
            if dirty sort:
                it means marks are not placed in continuous, so we sort marks
                by sequence.
            else:
                the marks are already continuous, then we sort by path
                (segements count) and titles (a.k.a. their dirnames).
                the priority that sort based:
                    (bool title_not_empty, int path_depth_is_low,
                     str title_lowercase_in_alphabet)
        """
        from copy import deepcopy
        if self.is_dirty_sort:
            items = deepcopy(self._items)  # type: list[dict]
            # 1. sort all marks (no matter valid or invalid) in alphabet order.
            # 2. put valid marks first and sort them by self.MARK_2_INDEX.
            items.sort(key=lambda x: x['mark'])
            items.sort(key=lambda x: self.MARK_2_INDEX.get(x['mark'], 999))
            # # items.sort(key=lambda x: (
            # #     0 if x['mark'] else 1,
            # #     self.MARK_2_INDEX.get(x['mark'], 999),
            # # ))
            # the sort has affected uid_2_index.
            for i, x in enumerate(items):
                self.uid_2_index[x['uid']] = i
            self.update_many(0, len(items), items)
            self.is_dirty_sort = False
        else:
            # tip:
            #   - only the first 26 items need to re-sort.
            #   - the first 26 items have convered all valid marks.
            #   - we can just rebuild and refresh the first 26 items.
            changed_length = len(self.MARK_2_INDEX)  # -> 26
            items = deepcopy(self._items[:changed_length])  # type: list[dict]
            # print(':vl', 'before', items)
            # inspired by: https://cloud.tencent.com/developer/ask/219983
            items.sort(key=lambda x: (
                0 if x['mark'] in self.MARK_2_INDEX else 1,
                0 if x['title'] else 1,
                x['dirpath'].lower(),
            ))
            # the sort has affected mark_2_uid, uid_2_index.
            for x, mark in zip(items, self.MARK_2_INDEX.keys()):
                x['mark'] = mark
            # print(':vl', 'after', items)
            for i, x in enumerate(items):
                self.uid_2_index[x['uid']] = i
            self.update_many(0, changed_length, items)
        self.resorted.emit(self)


class Model4(BaseModel):
    """ special items. """
    model_index = 3
    
    def __init__(self, gallery_dir: str):
        super().__init__(mark_2_index={',': 0, '.': 1})
        from ..paths import recycle_bin
        self.update(0, {'title': 'finalized', 'dirpath': gallery_dir})
        self.update(1, {'title': 'recycle bin', 'dirpath': recycle_bin})
    
    def move_paths(self, mark: str):
        # assert mark == '.'
        if mark == ',':
            raise Exception('cannot move finalized items!')
        else:
            return super().move_paths(mark)


def main(gallery_dir: str) -> tuple[Model1, Model2, Model3, Model4]:
    from os.path import exists
    from ..paths import sidebar_model as model_path
    models = (Model1(gallery_dir), Model2(), Model3(), Model4(gallery_dir))
    if exists(model_path):
        restore_from_local(models, model_path)
    return models


def restore_from_local(models, model_path: str):
    from lk_utils import loads
    from . import index
    
    data = loads(model_path)
    
    index.uid_2_paths = data['index']['uid_2_paths']
    index.uid_2_index = data['index']['uid_2_index']
    index.path_2_mark = data['index']['path_2_mark']
    index.mark_2_uid = data['index']['mark_2_uid']
    
    for model, kwargs in zip(models, data['models']):
        model.restore_from_local(**kwargs)


def save(models: tuple[Model1, Model2, Model3, Model4]):
    from lk_utils import dumps
    from ..paths import sidebar_model as model_path
    dumps({
        'index' : {
            'uid_2_paths': uid_2_paths,
            'uid_2_index': uid_2_index,
            'path_2_mark': path_2_mark,
            'mark_2_uid' : mark_2_uid,
        },
        'models': (
            {  # Model1
                'items': models[0].items,
            },
            {  # Model2
                'items': models[1].items,
            },
            {  # Model3
                'items'        : models[2].items,
                'is_dirty_sort': models[2].is_dirty_sort,
            },
            {  # Model4
                'items': models[3].items,
            }
        )
    }, model_path)
