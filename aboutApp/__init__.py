from os import path

app_name = path.dirname(__file__).replace('\\', '/').split('/')[-1]

default_app_config = app_name + '.apps.AboutappConfig'
