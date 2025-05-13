# import 1password

# all aws (apple with sauce)
from awth.config import initial_setup
from awth.util import log_error_and_exit
import boto3
from botocore.exceptions import ClientError, ParamValidationError

# import bw
import click
try:
    import configparser
    from configparser import NoOptionError, NoSectionError
except ImportError:
    import ConfigParser as configparser
    from ConfigParser import NoOptionError, NoSectionError
import datetime
import getpass
import keyring
import logging
from os import path, environ, makedirs
from pathlib import Path
from rich.prompt import Confirm, Prompt
import sys

logger = logging.getLogger('awth')
AWS_CREDS_PATH = path.expanduser(environ.get('AWS_SHARED_CREDENTIALS_FILE', '~/.aws/credentials'))


def setup_logger(level=logging.DEBUG):
    """
    set up basic logger
    """
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(
        logging.Formatter('%(levelname)s - %(message)s'))
    stdout_handler.setLevel(level)
    logger.addHandler(stdout_handler)
    logger.setLevel(level)


@click.command()
@click.option('--device',
              required=False,
              metavar='arn:aws:iam::123456788990:mfa/dudeman',
              help="The MFA Device ARN. This value can also be "
              "provided via the environment variable 'MFA_DEVICE' or"
              " the ~/.aws/credentials variable 'aws_mfa_device'.")
@click.option('--duration',
              type=int,
              help="The duration, in seconds, that the temporary "
                   "credentials should remain valid. Minimum value: "
                   "900 (15 minutes). Maximum: 129600 (36 hours). "
                   "Defaults to 43200 (12 hours), or 3600 (one "
                   "hour) when using '--assume-role'. This value "
                   "can also be provided via the environment "
                   "variable 'MFA_STS_DURATION'. ")
@click.option('--profile',
              help="If using profiles, specify the name here. The "
              "default profile name is 'default'. The value can "
              "also be provided via the environment variable "
              "'AWS_PROFILE'.",
              required=False)
@click.option('--long-term-suffix', '--long-suffix',
              help="The suffix appended to the profile name to"
              "identify the long term credential section",
              required=False)
@click.option('--short-term-suffix', '--short-suffix',
              help="The suffix appended to the profile name to"
              "identify the short term credential section",
              required=False)
@click.option('--assume-role', '--assume',
              metavar='arn:aws:iam::123456788990:role/RoleName',
              help="The ARN of the AWS IAM Role you would like to "
              "assume, if specified. This value can also be provided"
              " via the environment variable 'MFA_ASSUME_ROLE'",
              required=False)
@click.option('--role-session-name',
              help="Friendly session name required when using "
              "--assume-role",
              default=getpass.getuser(),
              required=False)
@click.option('--force',
              help="Refresh credentials even if currently valid.",
              required=False)
@click.option('--log-level',
              type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'], case_sensitive=False),
              help="Set log level",
              required=False,
              default='DEBUG')
@click.option('--setup',
              help="Setup a new log term credentials section",
              is_flag=bool,
              required=False)
@click.option('--token',
              help="Provide MFA token as an argument",
              required=False,
              default=None)
@click.option('--region',
              help="AWS STS Region",
              required=False,
              type=str)
@click.option('--keychain',
              is_flag=bool,
              help="Use system keychain to store or retrieve long term credentials",
              required=False)
def main(device: str,
         duration: int,
         profile: str,
         long_term_suffix: str,
         short_term_suffix: str,
         assume_role: str,
         role_session_name: str,
         force: bool,
         log_level: str,
         setup: bool,
         token: str = "",
         region: str = "eu-central-1",
         keychain: bool = False):

    # set up logging before we begin
    level = getattr(logging, log_level)
    setup_logger(level)

    if not path.isfile(AWS_CREDS_PATH):
        create_credentials_file = Confirm.ask(
                "Could not locate credentials file at "
                f"[green]{AWS_CREDS_PATH}[/green]. Would you like to create one?"
                )

        if create_credentials_file:
            # try creating directory and file
            try:
              makedirs(path.expanduser("~/.aws"), exist_ok=True)
              Path(AWS_CREDS_PATH).touch()
            except Exception as e:
                log_error_and_exit(logger,
                                   f'{e}. Could not locate credentials file at '
                                   f'{AWS_CREDS_PATH}')

    config = get_config(AWS_CREDS_PATH)

    if setup:
        initial_setup(logger, config, AWS_CREDS_PATH, keychain)
        return

    validate(config,
             profile,
             long_term_suffix,
             short_term_suffix,
             assume_role,
             keychain,
             device,
             duration,
             force)


def get_config(aws_creds_path: str = ""):
    """
    get the configuration and parse it
    """
    config = configparser.RawConfigParser()

    try:
        config.read(aws_creds_path)
    except configparser.ParsingError:
        e = sys.exc_info()[1]
        log_error_and_exit(logger,
                           "There was a problem reading or parsing "
                           f"your credentials file: {e.args[0]}")
    return config


def validate(config,
             profile: str = "",
             long_term_suffix: str = "",
             short_term_suffix: str = "",
             assume_role: bool = False,
             keychain: bool = False,
             device: str = "",
             duration: int = 0,
             force: bool = False
             ):
    """
    validate all the options
    """

    # check profile
    if not profile:
        profile = environ.get('AWS_PROFILE', 'default')

    # check long_term_suffix
    if not long_term_suffix:
        long_term_name = f'{profile}-long-term'
    elif long_term_suffix.lower() == 'none':
        long_term_name = profile
    else:
        long_term_name = f'{profile}-{long_term_suffix}'


    # check short_term_suffix
    if not short_term_suffix or short_term_suffix.lower() == 'none':
        short_term_name = profile
    else:
        short_term_name = f'{profile}-{short_term_suffix}'

    if long_term_name == short_term_name:
        log_error_and_exit(logger,
                           "The value for '--long-term-suffix' cannot "
                           "be equal to the value for '--short-term-suffix'")

    # check assume role
    if assume_role:
        role_msg = f"with assumed role: {assume_role}"
    elif config.has_option(profile, 'assumed_role_arn'):
        role_msg = f"with assumed role: {config.get(profile, 'assumed_role_arn')}"
    else:
        role_msg = ""

    logger.info(f'Validating credentials for profile: {short_term_name} {role_msg}')

    reup_message = "Obtaining credentials for a new role or profile."

    try:
        if keychain:
            key_id = keyring.get_password('aws:access_key_id', long_term_name)
            access_key = keyring.get_password('aws:secret_access_key', long_term_name)
        else:
            key_id = config.get(long_term_name, 'aws_access_key_id')
            access_key = config.get(long_term_name, 'aws_secret_access_key')
    except NoSectionError:
        log_error_and_exit(logger,
                           f"Long term credentials session '[{long_term_name}]' is missing. "
                           "You must add this section to your credentials file "
                           "along with your long term 'aws_access_key_id' and "
                           "'aws_secret_access_key'")
    except NoOptionError as e:
        log_error_and_exit(logger, e)

    # get device from param, env var or config
    if not device:
        if environ.get('MFA_DEVICE'):
            device = environ.get('MFA_DEVICE')
        elif config.has_option(long_term_name, 'aws_mfa_device'):
            device = config.get(long_term_name, 'aws_mfa_device')
        else:
            log_error_and_exit(logger,
                               'You must provide --device or MFA_DEVICE or set '
                               '"aws_mfa_device" in ".aws/credentials"')

    # get assume_role from param or env var
    if not assume_role:
        if environ.get('MFA_ASSUME_ROLE'):
            assume_role = environ.get('MFA_ASSUME_ROLE')
        elif config.has_option(long_term_name, 'assume_role'):
            assume_role = config.get(long_term_name, 'assume_role')

    # get duration from param, env var or set default
    if not duration:
        if environ.get('MFA_STS_DURATION'):
            duration = int(environ.get('MFA_STS_DURATION'))
        else:
            duration = 3600 if assume_role else 43200

    # If this is False, only refresh credentials if expired. Otherwise
    # always refresh.
    force_refresh = False

    # Validate presence of short-term section
    if not config.has_section(short_term_name):
        logger.info(f"Short term credentials section {short_term_name} is missing, "
                    "obtaining new credentials.")
        if short_term_name == 'default':
            try:
                config.add_section(short_term_name)
            # a hack for creating a section named "default"
            except ValueError:
                configparser.DEFAULTSECT = short_term_name
                config.set(short_term_name, 'CREATE', 'TEST')
                config.remove_option(short_term_name, 'CREATE')
        else:
            config.add_section(short_term_name)
        force_refresh = True

    # Validate option integrity of short-term section
    else:
        required_options = ['assumed_role',
                            'aws_access_key_id',
                            'aws_secret_access_key',
                            'aws_session_token',
                            'aws_security_token',
                            'expiration']
        try:
            short_term = {}
            for option in required_options:
                short_term[option] = config.get(short_term_name, option)
        except NoOptionError:
            logger.warn("Your existing credentials are missing or invalid, "
                        "obtaining new credentials.")
            force_refresh = True

        try:
            current_role = config.get(short_term_name, 'assumed_role_arn')
        except NoOptionError:
            current_role = None

        if force:
            logger.info("Forcing refresh of credentials.")
            force_refresh = True
        # There are not credentials for an assumed role,
        # but the user is trying to assume one
        elif current_role is None and assume_role:
            logger.info(reup_message)
            force_refresh = True
        # There are current credentials for a role and
        # the role arn being provided is the same.
        elif current_role is not None and assume_role and current_role == assume_role:
            pass
        # There are credentials for a current role and the role
        # that is attempting to be assumed is different
        elif current_role is not None and assume_role and current_role != assume_role:
            logger.info(reup_message)
            force_refresh = True
        # There are credentials for a current role and no role arn is
        # being supplied
        elif current_role is not None and assume_role is None:
            logger.info(reup_message)
            force_refresh = True

    should_refresh = True

    # Unless we're forcing a refresh, check expiration.
    if not force_refresh:
        exp = datetime.datetime.strptime(
            config.get(short_term_name, 'expiration'), '%Y-%m-%d %H:%M:%S')
        diff = exp - datetime.datetime.utcnow()
        if diff.total_seconds() <= 0:
            logger.info("Your credentials have expired, renewing.")
        else:
            should_refresh = False
            logger.info(
                f"Your credentials are still valid for {diff.total_seconds()} seconds"
                f" they will expire at {exp}")

    if should_refresh:
        get_credentials(short_term_name,
                        key_id,
                        access_key,
                        token,
                        device,
                        duration,
                        assume_role,
                        short_term_suffix,
                        role_session_name,
                        region,
                        config)


def get_credentials(short_term_name,
                    lt_key_id,
                    lt_access_key,
                    token,
                    device,
                    duration,
                    assume_role,
                    short_term_suffix,
                    role_session_name,
                    region,
                    config):
    """
    Get credentials from AWS?
    """

    if token:
        logger.debug("Received token as argument")
        mfa_token = str(token)
    else:
        mfa_token = Prompt(f'Enter AWS MFA code for device [{device}] '
                           f'(renewing for {duration} seconds):')

    client = boto3.client(
        'sts',
        aws_access_key_id=lt_key_id,
        aws_secret_access_key=lt_access_key
    )

    if assume_role:

        logger.info("Assuming Role - Profile: %s, Role: %s, Duration: %s",
                    short_term_name, assume_role, duration)
        if role_session_name is None:
            log_error_and_exit(logger, "You must specify a role session name "
                               "via --role-session-name")

        try:
            response = client.assume_role(
                RoleArn=assume_role,
                RoleSessionName=role_session_name,
                DurationSeconds=duration,
                SerialNumber=device,
                TokenCode=mfa_token
            )
        except ClientError as e:
            log_error_and_exit(logger,
                               f"An error occured while assuming role: {e}")
        except ParamValidationError:
            log_error_and_exit(logger, "Token must be six digits")

        config.set(short_term_name, 'assumed_role', 'True')
        config.set(short_term_name, 'assumed_role_arn', assume_role)
    else:
        logger.info(f"Fetching Credentials - Profile: {short_term_name}, Duration: {duration}")
        try:
            response = client.get_session_token(
                DurationSeconds=duration,
                SerialNumber=device,
                TokenCode=mfa_token
            )
        except ClientError as e:
            log_error_and_exit(
                    logger,
                    f"An error occured while calling assume role: {e}"
                    )
        except ParamValidationError:
            log_error_and_exit(logger, "Token must be six digits")

        config.set(short_term_name, 'assumed_role', 'False')
        config.remove_option(short_term_name, 'assumed_role_arn')

    # aws_session_token and aws_security_token are both added
    # to support boto and boto3
    options = [
        ('aws_access_key_id', 'AccessKeyId'),
        ('aws_secret_access_key', 'SecretAccessKey'),
        ('aws_session_token', 'SessionToken'),
        ('aws_security_token', 'SessionToken'),
    ]

    for option, value in options:
        config.set(
            short_term_name,
            option,
            response['Credentials'][value]
        )
    # Save expiration individiually, so it can be manipulated
    config.set(
        short_term_name,
        'expiration',
        response['Credentials']['Expiration'].strftime('%Y-%m-%d %H:%M:%S')
    )
    with open(AWS_CREDS_PATH, 'w') as configfile:
        config.write(configfile)
    logger.info(
        f"Success! Your credentials will expire in {duration} seconds at: "
        f"{response['Credentials']['Expiration']}")
    sys.exit(0)


if __name__ == "__main__":
    main()
