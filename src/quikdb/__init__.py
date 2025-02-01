import argparse
from .programs import program 
from .programs.prg_install import install_command

# if __name__ == "__main__":
args = program.parse_args()  # Parses command-line arguments

if hasattr(args, "func"):
    args.func(args)  # This calls the `install_command` or other associated function
else:
    program.print_help()  #

from .sdk import *