import os
import configparser


def read_config():

    #must have default value
    default={'data_path':'./data'}
    Config = configparser.ConfigParser(default)

    #hardcoded config file path
    config_path='./config.ini'
    f=None
    #create config file if not exist
    if os.path.isfile(config_path):
        Config.read(config_path)
    
    
    #read config
    #f=Config.read(config_path)
    with open(config_path, 'w') as configfile:    # save
        Config.write(configfile)
    return Config