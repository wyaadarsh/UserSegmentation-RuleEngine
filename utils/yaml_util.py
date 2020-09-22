import yaml


class YAMLReader:

    @classmethod
    def load_config_from_yml(cls, directory, file_name):
        with open(directory + file_name, 'r') as stream:
            try:
                config = yaml.load(stream)
                return config
            except yaml.YAMLError:
                print(("exception while loading config file " + file_name))
                return {}
