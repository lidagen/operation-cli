import json
import os.path

config_path = os.path.expanduser('~/.opscli/config.json')
config_directory = os.path.dirname(config_path)


def init(data: dict):
    if not os.path.exists(config_directory):
        os.makedirs(config_directory)

    with open(config_path, 'w') as f:
        json.dump(data, f, indent=4)


def append_config_item(new_data_pair: dict):
    with open(config_path, "r+") as f:
        data = json.load(f)
        data.update(new_data_pair)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def is_valid() -> bool:
    required_keys = [
        "env",
        "db_host",
        "db_username",
        "db_password"
    ]

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        return False

    for key in required_keys:
        if key not in config or not config[key]:
            return False

    return True


def read_config() -> dict:
    if not os.path.exists(config_directory):
        init({})

    with open(config_path, 'r') as f:
        config = json.load(f)
        return config