import configparser
import os

APP_PATH = os.path.expanduser(os.path.join('~', '.anpy'))
DATABASE_PATH = os.path.join(APP_PATH, 'data.db')
CONFIG_PATH = os.path.join(APP_PATH, 'config.ini')


def create_anpy_dir_if_not_exist(path=APP_PATH):
    os.makedirs(name=APP_PATH, exist_ok=True)


def create_config_file(excel_path, app_path=APP_PATH):
    excel_path = clean_excel_file(excel_path)
    config = configparser.ConfigParser()
    config['Paths'] = {'LogFile': excel_path}
    with open(os.path.join(app_path, 'config.ini'), 'w') as config_file:
        config.write(config_file)


def clean_excel_file(excel_path):
    if os.path.isdir(excel_path):
        excel_path = os.path.join(excel_path, 'log.xlsx')
    elif not (excel_path.endswith('.xlsx') or excel_path.endswith('.xlsm')):
        excel_path += '.xlsx'
    return excel_path
