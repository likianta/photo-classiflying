from os.path import dirname

from lk_utils import currdir

curr_dir = currdir()
proj_dir = dirname(curr_dir)

model = f'{proj_dir}/model'

sidebar_model = f'{model}/sidebar_model.pkl'
thumbnail_model = f'{model}/thumbnail_model.pkl'
user_config = f'{model}/user_config.yml'

recycle_bin = f'{model}/recycle_bin'
