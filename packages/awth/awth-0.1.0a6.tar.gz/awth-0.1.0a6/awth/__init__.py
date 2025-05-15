# import 1password

# internal modules
from awth.config import initial_setup, get_config, default_aws_config
from awth.constants import AWS_CREDS_PATH, LOG_LEVEL, LOG_FILE, USER
from awth.util import log_error_and_exit

# all AWS (apple with sauce)
import boto3
from botocore.exceptions import ClientError, ParamValidationError

# import bw
from click import option, command, Choice
import configparser
from configparser import NoOptionError, NoSectionError
import datetime
import keyring
import logging
from os import path, environ, makedirs
from pathlib import Path
from rich.prompt import Confirm, Prompt
from rich.logging import RichHandler
from .help_text import RichCommand, options_help
import sys

HELP = options_help()


def setup_logger(level="", log_file=""):
    """
    Sets up rich logger and stores the values for it in a db for future import
    in other files. Returns logging.getLogger("rich")
    """
    # determine logging level
    if not level:
        level = LOG_LEVEL

    log_level = getattr(logging, level.upper(), None)

    # these are params to be passed into logging.basicConfig
    opts = {'level': log_level, 'format': "%(message)s", 'datefmt': "[%X]"}

    # we only log to a file if one was passed into config.yml or the cli
    if not log_file:
        log_file = LOG_FILE

    # rich typically handles much of this but we don't use rich with files
    if log_file:
        opts['filename'] = log_file
        opts['format'] = "%(asctime)s %(levelname)s %(funcName)s: %(message)s"
    else:
        rich_handler_opts = {'rich_tracebacks': True}
        # 10 is the DEBUG logging level int value
        if log_level == 10:
            # log the name of the function if we're in debug mode :)
            opts['format'] = "[bold]%(funcName)s()[/bold]: %(message)s"
            rich_handler_opts['markup'] = True

        opts['handlers'] = [RichHandler(**rich_handler_opts)]

    # this uses the opts dictionary as parameters to logging.basicConfig()
    logging.basicConfig(**opts)

    if log_file:
        return None
    else:
        return logging.getLogger("rich")


@command(cls=RichCommand)
@option('--device',
        metavar='arn:aws:iam::123456788990:mfa/mirandel-smith',
        help="The MFA Device ARN. This value can also be "
        "provided via the environment variable 'MFA_DEVICE' or"
        " the ~/.aws/credentials variable 'aws_mfa_device'.")
@option('--duration',
        type=int,
        help="The duration, in seconds, that the temporary "
             "credentials should remain valid. Minimum value: "
             "900 (15 minutes). Maximum: 129600 (36 hours). "
             "Defaults to 43200 (12 hours), or 3600 (one "
             "hour) when using '--assume-role'. This value "
             "can also be provided via the environment "
             "variable 'MFA_STS_DURATION'. ")
@option('--profile',
        help="If using profiles, specify the name here. The "
        "default profile name is 'default'. The value can "
        "also be provided via the environment variable "
        "'AWS_PROFILE'.",
        default="default")
@option('--long-term-suffix', '--long-suffix', 'long_term_suffix',
        help="The suffix appended to the profile name to"
        "identify the long term credential section",
        default="long-term")
@option('--short-term-suffix', '--short-suffix', 'short_term_suffix',
        help="The suffix appended to the profile name to"
        "identify the short term credential section")
@option('--assume-role', '--assume',
        metavar='arn:aws:iam::123456788990:role/RoleName',
        help="The ARN of the AWS IAM Role you would like to "
        "assume, if specified. This value can also be provided"
        " via the environment variable 'MFA_ASSUME_ROLE'")
@option('--role-session-name', "role_session_name",
        help="Friendly session name required when using ",
        default=USER)
@option('--force',
        help="Refresh credentials even if currently valid.")
@option('--log-level', 'log_level',
        type=Choice(['CRITICAL', 'ERROR', 'WARN', 'INFO', 'DEBUG', 'NOTSET'],
                    case_sensitive=False),
        help="Set log level",
        default=LOG_LEVEL)
@option('--setup',
        help="Setup a new log term credentials section",
        is_flag=bool)
@option('--token', '--mfa-token',
        help="Provide MFA token as an argument",
        default="")
@option('--region',
        help="AWS STS Region",
        type=str)
@option('--keychain',
        is_flag=bool,
        help="Use system keychain to store or retrieve long term credentials")
def main(device: str,
         duration: int,
         profile: str = "default",
         long_term_suffix: str = "long-term",
         short_term_suffix: str = "",
         assume_role: str = "",
         role_session_name: str = USER,
         force: bool = False,
         log_level: str = LOG_LEVEL,
         setup: bool = False,
         token: str = "",
         region: str = "",
         keychain: bool = False):

    # set up logging before we begin
    logger = setup_logger(log_level)

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
              setup = True
            except Exception as e:
                log_error_and_exit(logger,
                                   f'{e}. Could not locate credentials file at '
                                   f'{AWS_CREDS_PATH}')

    credentials_obj = get_config(logger, AWS_CREDS_PATH)

    if setup:
        aws_config_obj, credentials_obj = initial_setup(logger, credentials_obj, region, keychain)
    else:
        aws_config_obj = default_aws_config(logger, profile, region)

    validate(logger,
             aws_config_obj,
             credentials_obj,
             profile,
             long_term_suffix,
             short_term_suffix,
             assume_role,
             keychain,
             device,
             duration,
             token,
             force)


def validate(log: logging.Logger,
             aws_config_obj: configparser.RawConfigParser,
             credentials_obj: configparser.RawConfigParser,
             profile: str = "",
             long_term_suffix: str = "",
             short_term_suffix: str = "",
             role_session_name: str = "",
             assume_role: bool = False,
             keychain: bool = False,
             device: str = "",
             duration: int = 0,
             token: str = "",
             force: bool = False
             ):
    """
    validate all the options
    """

    # check profile
    if not profile:
        profile = environ.get('AWS_PROFILE', 'default')

    # check long_term_suffix
    if long_term_suffix.lower() == 'none':
        long_term_name = profile
    else:
        long_term_name = f'{profile}-{long_term_suffix}'


    # check short_term_suffix
    if not short_term_suffix or short_term_suffix.lower() == 'none':
        short_term_name = profile
    else:
        short_term_name = f'{profile}-{short_term_suffix}'

    if long_term_name == short_term_name:
        log_error_and_exit(log,
                           "The value for '--long-term-suffix' cannot "
                           "be equal to the value for '--short-term-suffix'")

    # check assume role
    if assume_role:
        role_msg = f"with assumed role: {assume_role}"
    elif credentials_obj.has_option(profile, 'assumed_role_arn'):
        role_msg = f"with assumed role: {credentials_obj.get(profile, 'assumed_role_arn')}"
    else:
        role_msg = ""

    log.info(f'Validating credentials for profile: {short_term_name} {role_msg}')

    reup_message = "Obtaining credentials for a new role or profile."

    # if using the system keychain to store credentials
    if keychain:
        log.info(f"Checking system keychain for AWS {long_term_name} credentials...")
        key_id = keyring.get_password('aws:access_key_id', long_term_name)
        access_key = keyring.get_password('aws:secret_access_key', long_term_name)
        device = keyring.get_password('aws:mfa_device', long_term_name)

    # if using the AWS credentials file to store credentials
    else:
        try:
            log.info(f"Checking {AWS_CREDS_PATH} for AWS {long_term_name} credentials...")
            key_id = credentials_obj.get(long_term_name, 'aws_access_key_id')
            log.debug(f"key id: {key_id}")
            access_key = credentials_obj.get(long_term_name, 'aws_secret_access_key')
            log.debug(f"access_key: {access_key}")
            device = credentials_obj.get(long_term_name, 'aws_mfa_device')
            log.debug(f"device: {device}")
        except NoSectionError:
            log_error_and_exit(log,
                    f"Long term credentials session '{long_term_name}' is missing. "
                    "You must add this section to your credentials file "
                    "along with your long term 'aws_access_key_id' and "
                    "'aws_secret_access_key'")
        except NoOptionError as e:
            log_error_and_exit(log, e)

    # get device from param, env var or config
    if not device:
        if environ.get('MFA_DEVICE'):
            device = environ.get('MFA_DEVICE')
        elif credentials_obj.has_option(long_term_name, 'aws_mfa_device'):
            device = credentials_obj.get(long_term_name, 'aws_mfa_device')
        else:
            log_error_and_exit(log,
                               'You must provide --device or MFA_DEVICE or set '
                               '"aws_mfa_device" in ".aws/credentials"')

    # get assume_role from param or env var
    if not assume_role:
        if environ.get('MFA_ASSUME_ROLE'):
            assume_role = environ.get('MFA_ASSUME_ROLE')
        elif credentials_obj.has_option(long_term_name, 'assume_role'):
            assume_role = credentials_obj.get(long_term_name, 'assume_role')

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
    if not credentials_obj.has_section(short_term_name):
        log.info(f"Short term credentials section {short_term_name} is missing, "
                    "obtaining new credentials.")
        if short_term_name == 'default':
            try:
                credentials_obj.add_section(short_term_name)
            # a hack for creating a section named "default"
            except ValueError:
                configparser.DEFAULTSECT = short_term_name
                credentials_obj.set(short_term_name, 'CREATE', 'TEST')
                credentials_obj.remove_option(short_term_name, 'CREATE')
        else:
            credentials_obj.add_section(short_term_name)
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
                short_term[option] = credentials_obj.get(short_term_name, option)
        except NoOptionError:
            log.warn("Your existing credentials are missing or invalid, "
                        "obtaining new credentials.")
            force_refresh = True

        try:
            current_role = credentials_obj.get(short_term_name, 'assumed_role_arn')
        except NoOptionError:
            current_role = None

        if force:
            log.info("Forcing refresh of credentials.")
            force_refresh = True
        # There are not credentials for an assumed role,
        # but the user is trying to assume one
        elif current_role is None and assume_role:
            log.info(reup_message)
            force_refresh = True
        # There are current credentials for a role and
        # the role arn being provided is the same.
        elif current_role is not None and assume_role and current_role == assume_role:
            pass
        # There are credentials for a current role and the role
        # that is attempting to be assumed is different
        elif current_role is not None and assume_role and current_role != assume_role:
            log.info(reup_message)
            force_refresh = True
        # There are credentials for a current role and no role arn is
        # being supplied
        elif current_role is not None and assume_role is None:
            log.info(reup_message)
            force_refresh = True

    should_refresh = True

    # Unless we're forcing a refresh, check expiration.
    if not force_refresh:
        exp = datetime.datetime.strptime(
            credentials_obj.get(short_term_name, 'expiration'), '%Y-%m-%d %H:%M:%S')
        diff = exp - datetime.datetime.utcnow()
        if diff.total_seconds() <= 0:
            log.info("Your credentials have expired, renewing.")
        else:
            should_refresh = False
            log.info(
                f"Your credentials are still valid for {diff.total_seconds()} seconds"
                f" they will expire at {exp}")

    if should_refresh:
        region = aws_config_obj.get(profile, 'region')
        get_credentials(log,
                        credentials_obj,
                        short_term_name,
                        key_id,
                        access_key,
                        token,
                        device,
                        duration,
                        assume_role,
                        short_term_suffix,
                        role_session_name,
                        region)


def get_credentials(log: logging.Logger,
                    credentials_obj: configparser.RawConfigParser,
                    short_term_name: str,
                    lt_key_id: str,
                    lt_access_key: str,
                    token: str,
                    device: str,
                    duration: int,
                    assume_role: str,
                    short_term_suffix: str,
                    role_session_name: str = "",
                    region: str = ""):
    """
    Get credentials from AWS?
    """

    if token:
        log.debug("Received token as argument")
        mfa_token = str(token)
    else:
        mfa_token = Prompt.ask(
                f'Enter AWS MFA code for device [green]{device}[/green] (renewing for {duration} seconds)'
                )

    client = boto3.client(
        'sts',
        region_name=region,
        aws_access_key_id=lt_key_id,
        aws_secret_access_key=lt_access_key
    )

    if assume_role:

        log.info("Assuming Role - Profile: %s, Role: %s, Duration: %s",
                    short_term_name, assume_role, duration)
        if not role_session_name:
            log_error_and_exit(log, "You must specify a role session name "
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
            log_error_and_exit(log,
                               f"An error occured while assuming role: {e}")
        except ParamValidationError:
            log_error_and_exit(log, "Token must be six digits")

        credentials_obj.set(short_term_name, 'assumed_role', 'True')
        credentials_obj.set(short_term_name, 'assumed_role_arn', assume_role)
    else:
        log.info(f"Fetching Credentials - Profile: {short_term_name}, Duration: {duration}")
        try:
            response = client.get_session_token(
                DurationSeconds=duration,
                SerialNumber=device,
                TokenCode=mfa_token
            )
        except ClientError as e:
            log_error_and_exit(
                    log,
                    f"An error occured while calling assume role: {e}"
                    )
        except ParamValidationError as e:
            log_error_and_exit(log, f"Token must be six digits: {e}")

        credentials_obj.set(short_term_name, 'assumed_role', 'False')
        credentials_obj.remove_option(short_term_name, 'assumed_role_arn')

    # aws_session_token and aws_security_token are both added
    # to support boto and boto3
    # TODO: figure out which is for boto so we can get rid of it.
    options = [
        ('aws_access_key_id', 'AccessKeyId'),
        ('aws_secret_access_key', 'SecretAccessKey'),
        ('aws_session_token', 'SessionToken'),
        ('aws_security_token', 'SessionToken'),
    ]

    for option_tuple in options:
        credentials_obj.set(
            short_term_name,
            option_tuple[0],
            response['Credentials'][option_tuple[1]]
        )

    # Save expiration individiually, so it can be manipulated
    credentials_obj.set(
        short_term_name,
        'expiration',
        response['Credentials']['Expiration'].strftime('%Y-%m-%d %H:%M:%S')
    )
    with open(AWS_CREDS_PATH, 'w') as configfile:
        credentials_obj.write(configfile)
    log.info(
        f"Success! Your credentials will expire in {duration} seconds at: "
        f"{response['Credentials']['Expiration']}")
    sys.exit(0)


if __name__ == "__main__":
    main()
