def mark_2_group_index(mark: str) -> int:
    """
    mark    group_index
    0       0
    1-9     1
    a-z     2
    ,.      3
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
