"""
help text functions for the onboardme cli
"""
# file for rich printing
import awth
import click
from importlib.metadata import version as get_version
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

# custom local module
VERSION = get_version("awth")

# this is for creating new help text svgs for the READMEs
RECORD = False


def pretty_choices(default_list: list) -> str:
    """
    Takes a list of default choices and surrounds them with a meta markup tag
    and join them with a comma for a pretty return "Choices" string.
    Example: pretty_choices(['beep', 'boop']) returns:
             'Choices: [meta]beep[/meta], [meta]boop[/meta]'
    """
    defaults = '[/meta], [meta]'.join(default_list)
    return 'Choices: [meta]' + defaults + '[/meta]'


def options_help() -> dict:
    """
    Help text for all the options/switches for main()
    """
    log_levels = pretty_choices(['CRITICAL', 'ERROR', 'WARNING', 'INFO',
                                 'DEBUG', 'NOTSET'])

    return {
            "device": "The MFA Device ARN. This value can also be provided via "
                      "the environment variable 'MFA_DEVICE' or the "
                      "~/.aws/credentials variable 'aws_mfa_device'.",

            'duration': "The duration, in seconds, that the temporary "
                        "credentials should remain valid. Minimum value: "
                        "900 (15 minutes). Maximum: 129600 (36 hours). "
                        "Defaults to 43200 (12 hours), or 3600 (one "
                        "hour) when using '--assume-role'. This value "
                        "can also be provided via the environment "
                        "variable 'MFA_STS_DURATION'. ",

            'profile': "If using profiles, specify the name here. The "
                       "default profile name is 'default'. The value can "
                       "also be provided via the environment variable "
                       "'AWS_PROFILE'.",

            'long-term-suffix': "The suffix appended to the profile name to"
                                "identify the long term credential section",
            'short-term-suffix': "The suffix appended to the profile name to"
                                 "identify the short term credential section",
            'assume-role': "The ARN of the AWS IAM Role you would like to "
                           "assume, if specified. This value can also be provided"
                           " via the environment variable 'MFA_ASSUME_ROLE'. "
                           "Example: 'arn:aws:iam::123456788990:role/RoleName'",
            'role-session-name': "Friendly session name required when using --assume-role",
            'force': "Refresh credentials even if currently valid.",
            'log-level': f"Set log level. {log_levels}",
            'setup': "Setup a new log term credentials section",
            'token': "Provide MFA token as an argument",
            'region': "AWS STS Region",
            'keychain': "Use system keychain to store or retrieve long term credentials"
              }


class RichCommand(click.Command):
    """
    Override Clicks help with a Richer version.

    This is from the Textualize/rich-cli project on github.com:
    https://github.com/Textualize/rich-cli
    """

    def format_help(self, ctx, formatter):

        class OptionHighlighter(RegexHighlighter):
            highlights = [r"(?P<switch>\-\w)",
                          r"(?P<option>\-\-[\w\-]+)",
                          r"(?P<unstable>[b][e][t][a])"]

        highlighter = OptionHighlighter()

        console = Console(theme=Theme({"option": "green",
                                       "switch": "magenta",
                                       "meta": "blue",
                                       "unstable": "italic cyan"}),
                          highlighter=highlighter, record=RECORD)

        title = "🌤️ [green]awth[/] 🗝️\n"
        desc = (
            "[steel_blue]Authenticate to AWS using MFA.")

        console.print(title + desc, justify="center")

        console.print("\n[b]Usage[/]:  [magenta]awth[/] " +
                      "[green][OPTIONS]\n")

        options_table = Table(highlight=True, box=None, show_header=False,
                              row_styles=["", "dim"],
                              padding=(1, 1, 0, 0))

        # this used to be self.get_params(ctx)[1:] to have only one hidden option
        for param in self.get_params(ctx):

            if len(param.opts) == 2:
                opt1 = highlighter(param.opts[1])
                opt2 = highlighter(param.opts[0])
            else:
                opt2 = highlighter(param.opts[0])
                opt1 = Text("")

            if param.metavar:
                opt2 += Text(f" {param.metavar}",
                             style="meta")

            options = Text(" ".join(reversed(param.opts)))
            help_record = param.get_help_record(ctx)
            if help_record is None:
                help = ""
            else:
                help = Text.from_markup(param.get_help_record(ctx)[-1],
                                        emoji=False)

            if param.metavar:
                options += f" {param.metavar}"

            options_table.add_row(opt1, opt2, highlighter(help))

        url = (" ♥ docs: [link=https://github.com/small-hack/awth]"
               "small-hack/awth[/link]")

        console.print(Panel(options_table,
                            border_style="dim light_steel_blue",
                            title="⌥  Options",
                            title_align="left",
                            subtitle=url,
                            subtitle_align="right"))

        # I use this to print a pretty svg at the end sometimes
        if RECORD:
            console.save_svg("screenshots/awth.svg", title="term")
