import argparse
# import readline
# import os
from email_validator import validate_email, EmailNotValidError
from quikdb.utils.toolbox import Tools  # Assuming Tools is defined with necessary methods

def config_command(args):
    """Dynamically add a config entry."""
    # Argument parser for the `config` command
    # parser = argparse.ArgumentParser(description="Dynamically add a config entry.")
    # parser.add_argument("-u", "--username", type=str, help="username for the account", required=True)
    # parser.add_argument("-e", "--email", type=str, help="email for the account")
    # parser.add_argument("-i", "--identity", type=str, help="identity for the account")
    # args = parser.parse_args()

    # Validate required arguments
    if not args.email and not args.identity:
        print("Error: email or identity is required.")
        return

    # Prompt for project token
    project_token_ref = input("Please enter your project token: ").strip()
    if not project_token_ref:
        print("Error: Token is required to proceed.")
        return

    # Clear the config file
    open(Tools.CONFIG_FILE, 'w').close()

    # Append validated email or identity
    if args.email:
        try:
            validate_email(args.email)
            Tools.append_to_config_file("email", args.email)
        except EmailNotValidError:
            print("Error: Invalid email provided.")
            return
    elif args.identity:
        Tools.append_to_config_file("identity", args.identity)

    # Append username and project token
    Tools.append_to_config_file("username", args.username)
    Tools.append_to_config_file("projectTokenRef", project_token_ref)
    print("Config success!")

# Example of how to add this command to a CLI program
# if __name__ == "__main__":
# config_command()
