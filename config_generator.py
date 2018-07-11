import yaml
import os

from hyperopt_conf import definition


class ConfigGenerator(object):
    def __init__(self, trainer_config_path=None):
        if trainer_config_path:
            self.trainer_config_path = trainer_config_path
        else:
            DEFAULT_CONF_PATH = 'trainer_config.yaml'
            self.trainer_config_path = DEFAULT_CONF_PATH


    def generate(self, env_name, params, output_file_name):
        params = params[0]
        output_conf_path = 'configs/' + output_file_name + '.yaml'
        config_data_root = yaml.load(open(self.trainer_config_path))

        if env_name in config_data_root:
            config_data = config_data_root[env_name]
        else:
            config_data = config_data_root['default']

        for i, variable in enumerate(definition):
            config_data[variable['name']] = params[i]

        os.makedirs(os.path.dirname(output_conf_path), exist_ok=True)
        with open(output_conf_path, 'w') as output_file:
            yaml.dump(config_data_root, output_file, default_flow_style=False)

        return output_conf_path
