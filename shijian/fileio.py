import os.path
import shutil
import json
from datetime import date
from json import JSONEncoder

from task import FloatingTask, DatedTask, Task

SAVE_FOLDER = os.path.expanduser('~/.shijian')
SAVE_FILE = os.path.join(SAVE_FOLDER, 'tasks.json')
SAVE_FILE_TEMP = os.path.join(SAVE_FOLDER, 'tasks.json.temp')


def save(data):
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    with open(SAVE_FILE_TEMP, 'w') as f:
        json.dump(data, f, cls=Encoder, sort_keys=True, indent=4)
    shutil.move(SAVE_FILE_TEMP, SAVE_FILE)


def load():
    os.makedirs(SAVE_FOLDER, exist_ok=True)
    if not os.path.isfile(SAVE_FILE):
        return None
    with open(SAVE_FILE, 'r') as f:
        return json.load(f, object_hook=decode)


def decode(dct):
    if 'type' in dct:
        if dct['type'] == 'date':
            return date.fromisoformat(dct['value'])
        if dct['type'] == 'floating':
            return FloatingTask(dct['name'], dct['identifier'],
                                dct['hours_remaining'])

        if dct['type'] == 'dated':
            # due_date = decode(dct['due_date'])
            return DatedTask(dct['name'],
                             dct['identifier'],
                             dct['due_date'],
                             dct['hours_remaining'])
    return dct


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return {"type": "date", "value": o.isoformat()}

        if isinstance(o, Task):
            return o.__dict__

        return JSONEncoder.default(self, o)
