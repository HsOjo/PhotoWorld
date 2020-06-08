import os

from flask import Config, Flask

current_app: Flask


def get_config(key, default=None):
    config = current_app.config  # type: Config
    return config.get(key, default)


def get_program_path():
    app_path = current_app.root_path  # type: str
    path = os.path.join(app_path, '..')
    return path


def get_data_path():
    return os.path.join(get_program_path(), get_config('DATA_DIR'))


def register_all_callable_object_from_package(pkg, is_filter=False):
    for k in dir(pkg):
        f = getattr(pkg, k)
        if callable(f):
            if is_filter:
                current_app.add_template_filter(f)
            else:
                current_app.add_template_global(f)
