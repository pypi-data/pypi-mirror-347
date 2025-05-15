from awth.util import log_error_and_exit
import logging

from rich.prompt import Prompt, Confirm

# this parses the weird aws credentials file
import configparser

from .constants import AWS_CREDS_PATH, AWS_CONFIG_PATH

import getpass
import keyring

from os import environ

from sys import exc_info


def initial_setup(log: logging.Logger,
                  credentials_obj: configparser.RawConfigParser,
                  region: str = "",
                  keychain: bool = False):
    """
    setup the ~/.aws/credentials file and ~/.aws/config file

    returns config objects for both
    """
    profile = Prompt.ask('Profile name to', default="default")
    profile_name = f"{profile}-long-term"

    aws_access_key_id = getpass.getpass('aws_access_key_id: ')

    if aws_access_key_id is None or aws_access_key_id == "":
        log_error_and_exit(log, "You must supply aws_access_key_id")

    aws_secret_access_key = getpass.getpass('aws_secret_access_key: ')

    while not aws_secret_access_key:
        log_error_and_exit(log, "You must supply aws_secret_access_key")
        aws_secret_access_key = getpass.getpass('aws_secret_access_key: ')

    aws_mfa_device = getpass.getpass('AWS MFA device ARN: ')

    if keychain:
        keyring.set_password("aws:access_key_id", profile_name, aws_access_key_id)
        keyring.set_password("aws:secret_access_key", profile_name, aws_secret_access_key)
        keyring.set_password("aws:mfa_device", profile_name, aws_mfa_device)
    else:
        # add section with name they gave us plus "-long-term"
        credentials_obj.add_section(profile_name)
        credentials_obj.set(profile_name, 'aws_access_key_id', aws_access_key_id)
        credentials_obj.set(profile_name, 'aws_secret_access_key', aws_secret_access_key)
        credentials_obj.set(profile_name, 'aws_mfa_device', aws_mfa_device)
        with open(AWS_CREDS_PATH, 'w') as configfile:
            credentials_obj.write(configfile)

    aws_config_file_obj = default_aws_config(log, profile, region)

    return aws_config_file_obj, credentials_obj


def default_aws_config(log: logging.Logger, profile: str, region: str):
    """
    get AWS region from env var or ~/.aws/config file
    """
    # make sure we have a region before we proceed
    aws_config_file_obj = get_config(log, AWS_CONFIG_PATH)
    region_msg = (
            'You must provide a default region either by passing in '
            '--region, setting $AWS_REGION, or setting "region" in "~/.aws/config"'
            )

    if not region:
        # check env var for region
        region = environ.get('AWS_REGION', '')
        if region:
            log.info(f"Found default AWS region ({region}) in $AWS_REGION env var.")

        # check ~/.aws/config for region
        if not region:
            if aws_config_file_obj.has_section(profile):
                region = aws_config_file_obj.get(profile, 'region', fallback="")
                if region:
                    log.info(f"Found default AWS region ({region}) in ~/.aws/config "
                             f"under {profile} section.")

        # finally just try and ask the user for region
        if not region:
            region = Prompt.ask(f"{profile} AWS region", default="eu-central-1")
            if not region:
                log_error_and_exit(log, region_msg)
            else:
                yes = Confirm.ask(
                        f"Do you want to save this region for {profile}"
                        "in ~/.aws/config for next time?")
                if yes:
                    # add section if it exists
                    if not aws_config_file_obj.has_section(profile):
                      aws_config_file_obj.add_section(profile)

                    aws_config_file_obj.set(profile, 'region', region)

                    with open(AWS_CONFIG_PATH, 'w') as configfile:
                        aws_config_file_obj.write(configfile)

    return aws_config_file_obj


def get_config(logger: logging.Logger, aws_creds_path: str = ""):
    """
    get the configuration from the aws credentials file and parse it
    """
    config = configparser.ConfigParser()

    try:
        config.read(aws_creds_path)
    except configparser.ParsingError:
        e = exc_info()[1]
        log_error_and_exit(logger,
                           "There was a problem reading or parsing "
                           f"your credentials file: {e.args[0]}")

    return config
