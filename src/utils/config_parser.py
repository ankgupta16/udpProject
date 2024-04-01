import configparser


class ConfigParser:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../src/conf/conf.ini')

    def get_prop_value(self, section, key):
        return self.config.get(section, key, fallback=None)
