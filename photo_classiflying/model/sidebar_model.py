from lk_qtquick_scaffold import Model
from lk_qtquick_scaffold import signal

path_2_mark = {}


class BaseModel(Model):
    def __init__(self, mark_2_index: dict[str, int]):
        super().__init__(role_names=('mark', 'count', 'title', 'dirpath'))
        self.mark_2_index = mark_2_index
        self.mark_2_paths = {x: set() for x in self.mark_2_index}
        for mark in self.mark_2_index:
            self.append({
                'mark'   : mark,
                'count'  : 0,
                'title'  : '',
                'dirpath': ''
            })
    
    def reload_mark_paths(self, mark_paths: dict[str, set[str]]):
        self.mark_2_paths = mark_paths
        for mark, paths in self.mark_2_paths.items():
            self.update(
                index=self.mark_2_index[mark],
                item={'count': len(paths)}
            )
    
    def increase_mark_count(self, mark: str, path: str):
        try:
            self.mark_2_paths[mark].add(path)
        except KeyError:
            print(':pv4l', mark, tuple(self.mark_2_paths.keys()))
            return
        self.update(
            index=self.mark_2_index[mark],
            item={'count': len(self.mark_2_paths[mark])}
        )
    
    def decrease_mark_count(self, mark: str, path: str):
        self.mark_2_paths[mark].remove(path)
        assert len(self.mark_2_paths[mark]) >= 0
        self.update(
            index=self.mark_2_index[mark],
            item={'count': len(self.mark_2_paths[mark])}
        )
    
    def move_paths(self, mark: str):
        from os.path import basename
        from shutil import move
        
        index = self.mark_2_index[mark]
        dir_o = self.get(index)['dirpath']
        paths = tuple(self.mark_2_paths[mark])
        for path in paths:
            file_i = path
            file_o = '{}/{}'.format(dir_o, name := basename(path))
            print(':v2', 'move', name)
            move(file_i, file_o)
            
        self.mark_2_paths.clear()
        self.update(self.mark_2_index[mark], {'count': 0})
        return paths


class Model1(BaseModel):
    def __init__(self, gallery_dir: str):
        super().__init__(mark_2_index={'0': 0})
        # self._gallery_dir = gallery_dir
        self.update(0, {'title': 'default', 'dirpath': gallery_dir})
    
    def init_paths(self, paths):
        self.mark_2_paths['0'].update(paths)
        self.update(0, {'count': len(paths)})
    
    def add_file(self, path: str):
        mark = '0'
        path_2_mark[path] = mark
        self.mark_2_paths[mark].add(path)
        self.update(0, {'count': len(self.mark_2_paths[mark])})
    
    def remove_file(self, path: str):
        mark = '0'
        path_2_mark.pop(path)
        self.mark_2_paths[mark].remove(path)
        self.update(0, {'count': len(self.mark_2_paths[mark])})


class Model2(Model):
    def __init__(self):
        super().__init__(role_names=('mark', 'count', 'title', 'dirpath'))
        self.recent_marks = []
        self.append_many(
            [{'mark': '', 'count': 0, 'title': '', 'dirpath': ''}] * 9
        )
    
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


class Model3(BaseModel):
    mark_updated = signal(str, int, str, str)  # mark, count, title, dirpath
    
    def __init__(self):
        from os.path import basename
        from ..config import user_config
        
        super().__init__(
            mark_2_index={str(x): i for i, x in enumerate((
                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            ))}
        )
        
        predefined_paths = user_config['predefined_paths']
        for i, path in enumerate(predefined_paths[:len(self.mark_2_index)]):
            self.update(index=i, item={
                'dirpath': path,
                'title'  : basename(path),
            })
        for path in predefined_paths[len(self.mark_2_index):]:
            self.append({
                'mark'   : '',
                'count'  : 0,
                'dirpath': path,
                'title'  : basename(path),
            })
    
    def increase_mark_count(self, mark: str, path: str):
        super().increase_mark_count(mark, path)
        item = self.get(self.mark_2_index[mark])
        self.mark_updated.emit(
            mark, item['count'], item['title'], item['dirpath']
        )
        
    def decrease_mark_count(self, mark: str, path: str):
        super().decrease_mark_count(mark, path)
        item = self.get(self.mark_2_index[mark])
        self.mark_updated.emit(
            mark, item['count'], item['title'], item['dirpath']
        )
    
    def sort_marks(self):
        backup = self._items[1:-1]
        # print(':vl', backup)
        #   top and bottom don't participate in the sort.
        backup.sort(key=lambda x: (not bool(x['dirpath']), x['dirpath']))
        # backup.sort(key=lambda x: (not bool(x['title']), x['title']))
        # print(':vl', backup)
        #   sort by: tuple[bool is_empty, str text]
        #       is_empty: True first, False last
        #   https://cloud.tencent.com/developer/ask/219983
        # rebuild marks in order.
        for item, mark in zip(
                [None] + backup + [None],
                self.mark_2_index.keys()
        ):
            if item is None: continue
            item['mark'] = mark
        self.update_many(1, 1 + len(backup), backup)


class Model4(BaseModel):
    def __init__(self):
        super().__init__(mark_2_index={',': 0, '.': 1})
        from ..paths import recycle_bin
        self._recycle_bin = recycle_bin
    
    def move_paths(self, mark: str):
        if mark == ',':
            raise Exception('cannot move finalized items')
        
        from os.path import basename
        from shutil import move
        
        dir_o = self._recycle_bin
        paths = tuple(self.mark_2_paths[mark])
        for path in paths:
            file_i = path
            file_o = '{}/{}'.format(dir_o, name := basename(path))
            print(':v2', 'move', name)
            move(file_i, file_o)
            
        self.mark_2_paths.clear()
        self.update(self.mark_2_index[mark], {'count': 0})
        return paths


def main(gallery_dir: str) -> tuple[Model1, Model2, Model3, Model4]:
    from os.path import exists
    from ..paths import sidebar_model as model_path
    models = (Model1(gallery_dir), Model2(), Model3(), Model4())
    if exists(model_path):
        restore_from_local(models, model_path)
    return models


def restore_from_local(models, model_path: str):
    from lk_utils import loads
    global path_2_mark
    data = loads(model_path)
    path_2_mark = data['path_2_mark']
    
    models[0].reload_mark_paths(data['models'][0])
    models[2].reload_mark_paths(data['models'][2])
    models[3].reload_mark_paths(data['models'][3])
    
    models[1].recent_marks = data['models'][1]['recent_marks']
    models[1].update_many(0, 9, data['models'][1]['items'])


def save(models: tuple[Model1, Model2, Model3, Model4]):
    from lk_utils import dumps
    from ..paths import sidebar_model as model_path
    dumps({
        'path_2_mark': path_2_mark,
        'models'     : (
            models[0].mark_2_paths,
            {
                'recent_marks': models[1].recent_marks,
                'items'       : models[1].items,
            },
            models[2].mark_2_paths,
            models[3].mark_2_paths,
        )
    }, model_path)
