import yaml
import os

default_config = 'config.yaml'
default_config_path = os.path.join(os.getcwd(), default_config)

config = {}
config['server'] = {}
config['server']['host'] = '0.0.0.0'
config['server']['port'] = 5000

config['server']['socket'] = {}
config['server']['socket']['pull'] = 'tcp://*:5557'
config['server']['socket']['pub'] = 'tcp://*:5558'

config['server']['session'] = {}
config['server']['session']['access-token-expires'] = 3600

config['server']['security'] = {}
config['server']['security']['jwt-key'] = 'super-secret'
config['server']['security']['jwt-blacklist'] = True
config['server']['debug'] = True

config['database'] = {}
config['database']['connector'] = 'postgresql'
config['database']['username'] = 'postgres'
config['database']['password'] = 'password'
config['database']['host'] = '127.0.0.1'
config['database']['port'] = 5432
config['database']['name'] = 'store'
config['database']['path'] = 'store.db'
config['database']['salt'] = 'pepper&salt'

def readConfig(path=None):
    if not path:
        path = default_config_path
    with open(path, 'r') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

def writeConfig(config, path=None):
    if not path:
        path = default_config_path
    with open(path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
