import argparse
from .prg_install import install_command
from .prg_config import config_command


# Create the CLI program
def create_program():
    parser = argparse.ArgumentParser(
        description="QuikDB CLI."
    )
    parser.add_argument(
        "--version","-v", action="version", version="1.0.0", help="Show program version"
    )
    return parser

program = create_program()
subparsers = program.add_subparsers(
    title="subcommands", help="this is used for configurations and installation of quickdb"
)
install_parser = subparsers.add_parser('install', help='This checks if quikdb is installed, installs it if necessary')
install_parser.set_defaults(func=install_command)

config_parser = subparsers.add_parser(
    'config', help='This configures QuikDB settings'
)
config_parser.add_argument(
    '--email', "-e", required=True, help="User email for QuikDB configuration"
)
config_parser.add_argument(
    '--username', "-u",  required=True, help="Username for QuikDB configuration"
)
config_parser.add_argument(
    "-i", "--identity", type=str,  help="identity for the account"
)
config_parser.set_defaults(func=config_command)


# program.add_argument("install", type=str, help="This checks if quikdb is installed, installs it if necessary ",action=install_command())


