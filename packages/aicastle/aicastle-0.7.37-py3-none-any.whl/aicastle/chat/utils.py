import yaml

from aicastle.chat.filepaths import get_chat_filepaths
from aicastle.utils.hash import get_hash_file

def load_config(config_path='.aicastle/chat/config.yml'):
    with open(config_path, 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
    return config_data

def get_chat_file_hashes():
    filepaths = get_chat_filepaths()
    return {filepath:get_hash_file(filepath) for filepath in filepaths}

def load_system_text(system_text_path='.aicastle/chat/system.txt'):
    with open(system_text_path, 'r', encoding='utf-8') as file:
        system_text = file.read()
    return system_text