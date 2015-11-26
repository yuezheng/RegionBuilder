import json

config_file = "./config.json"

class Config(object):
    def __init__(self, data):
        self.regions = data.get('regions', [])
        self.auth = data.get('auth')

    def list_regions(self):
        return self.regions

    def auth_info(self):
        return self.auth


def get_config():
    with open(config_file) as data_file:
        data = json.load(data_file)
    config = Config(data)
    return config
