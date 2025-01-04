import os
import pty
import subprocess

def install_dfx():
    """Install the `dfx` tool."""
    try:
        # Create a pseudo-terminal to simulate interactivity
        master, slave = pty.openpty()
        install_command = 'sh -ci "$(curl -fsSL https://internetcomputer.org/install.sh)"'
        
        process = subprocess.run(
            install_command,
            shell=True,
            stdout=None,
            stderr=None,
            text=True
        )
        
        # Read output from the master
        # os.close(slave)
        # output = os.read(master, 1024).decode()
        # print(output)
        
        if process.returncode != 0:
            print("Error installing dfx.")
            exit(1)
        else:
            print("dfx installed successfully.")

    except Exception as e:
        print(f"An error occurred during dfx installation: {e}")
