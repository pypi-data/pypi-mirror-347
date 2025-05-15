def _get_resources_dir():
    import localsend

    return localsend.__module_dir__ / "resources"


def get_adjectives_path():
    return _get_resources_dir() / "adjectives.txt"


def get_object_names_path():
    return _get_resources_dir() / "object_names.txt"
