import getpass
from os import path, environ

AWS_CREDS_PATH = path.expanduser(environ.get('AWS_SHARED_CREDENTIALS_FILE', '~/.aws/credentials'))
AWS_CONFIG_PATH = path.expanduser(environ.get('AWS_SHARED_CONFIG_FILE', '~/.aws/config'))
LOG_LEVEL = 'info'
LOG_FILE = None
USER = getpass.getuser()
