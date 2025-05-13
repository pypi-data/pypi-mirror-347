from awth.util import log_error_and_exit

from rich.prompt import Prompt

try:
    import configparser
    from configparser import NoOptionError, NoSectionError
except ImportError:
    import ConfigParser as configparser  # noqa
    from ConfigParser import NoOptionError, NoSectionError  # noqa

import getpass
import keyring


def initial_setup(logger, config, config_path, no_keychain=False):
    profile_name = Prompt('Profile name to [default]: ')
    if profile_name is None or profile_name == "":
        profile_name = "default"

    profile_name = f"{profile_name}-long-term"
    aws_access_key_id = getpass.getpass('aws_access_key_id: ')

    if aws_access_key_id is None or aws_access_key_id == "":
        log_error_and_exit(logger, "You must supply aws_access_key_id")

    aws_secret_access_key = getpass.getpass('aws_secret_access_key: ')

    if aws_secret_access_key is None or aws_secret_access_key == "":
        log_error_and_exit(logger, "You must supply aws_secret_access_key")

    if no_keychain:
        config.add_section(profile_name)
        config.set(profile_name, 'aws_access_key_id', aws_access_key_id)
        config.set(profile_name, 'aws_secret_access_key', aws_secret_access_key)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    else:
        keyring.set_password("aws:access_key_id", profile_name, aws_access_key_id)
        keyring.set_password("aws:secret_access_key", profile_name, aws_secret_access_key)
