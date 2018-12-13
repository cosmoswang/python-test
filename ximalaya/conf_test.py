import configparser

config = configparser.ConfigParser()
config.read('./.res/.conf')
print(config.get('info', 'pass'))