from os.path import expanduser, join, isfile
from os import makedirs
import toml

CONFIG_FILE_ERROR = "There's something wrong with your config file."


def read_subjects_from_toml(path):
    if not isfile(path):
        make_default_toml(path)

    try:
        with open(path, 'r') as f:
            d = toml.load(f, dict)
            return d['subjects']
    except (TypeError, toml.TomlDecodeError, ValueError):
        print(CONFIG_FILE_ERROR)
        exit(1)


def make_default_toml(path):
    d = {"subjects": []}
    with open(path, 'w') as f:
        toml.dump(d, f)


__directory = join(expanduser("~"), '.surv_time_tracking')
__toml_file = join(__directory, "config.toml")
makedirs(__directory, exist_ok=True)


# Exports
subjects = read_subjects_from_toml(__toml_file)
FILE = join(__directory, 'data.txt')
