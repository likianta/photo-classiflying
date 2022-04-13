uid_2_paths = {}  # type: dict[str, set[str]]
uid_2_index = [{}, {}, {}, {}]  # type: list[dict[str, int]]
#   [{str uid: int index, ...}, ...]
#       the list index is `model_index`
path_2_mark = {}  # type: dict[str, str]
mark_2_uid = {}  # type: dict[str, str]


def mark_2_modelx(mark: str) -> int:
    """ return model index based on mark characteristic.
    
    mark    modelx  note
    0       0
    1-9     1
    a-z     2
    ,.      3       comma and period.
    """
    # noinspection PyCompatibility
    match mark:
        case '0':
            return 0
        case x if x.isdigit():
            return 1
        case x if x.isalpha():
            return 2
        case _:
            return 3
