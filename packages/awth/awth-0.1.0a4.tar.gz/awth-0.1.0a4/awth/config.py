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


def initial_setup(logger,
                  config,
                  config_path: str,
                  keychain: bool = False):
    """
    setup the credentials file
    """
    profile_name = Prompt.ask('Profile name to', default="default")
    profile_name = f"{profile_name}-long-term"

    aws_access_key_id = getpass.getpass('aws_access_key_id: ')

    if aws_access_key_id is None or aws_access_key_id == "":
        log_error_and_exit(logger, "You must supply aws_access_key_id")

    aws_secret_access_key = getpass.getpass('aws_secret_access_key: ')

    while not aws_secret_access_key:
        log_error_and_exit(logger, "You must supply aws_secret_access_key")
        aws_secret_access_key = getpass.getpass('aws_secret_access_key: ')

    aws_mfa_device = getpass.getpass('AWS MFA device ARN: ')

    if keychain:
        keyring.set_password("aws:access_key_id", profile_name, aws_access_key_id)
        keyring.set_password("aws:secret_access_key", profile_name, aws_secret_access_key)
        keyring.set_password("aws:mfa_device", profile_name, aws_mfa_device)
    else:
        # add section with name they gave us plus "-long-term"
        config.add_section(profile_name)
        config.set(profile_name, 'aws_access_key_id', aws_access_key_id)
        config.set(profile_name, 'aws_secret_access_key', aws_secret_access_key)
        config.set(profile_name, 'aws_mfa_device', aws_mfa_device)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
