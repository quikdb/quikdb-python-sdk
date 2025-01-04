import os
import pty
import sys
import re
import select
import subprocess

def create_principal(username: str):
    """
    Creates a new principal (dfx identity) in a pseudo-tty using only the standard library.
    Allows the user to type passphrases interactively, and captures the seed phrase.
    """
    # 1) Create a new pseudo-tty
    master_fd, slave_fd = pty.openpty()

    # 2) Spawn the 'dfx identity new <username>' command in that pseudo-tty
    process = subprocess.Popen(
        ["dfx", "identity", "new", username],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        text=True,  # So we deal with str instead of bytes in Python 3
    )

    # We close the slave FD in the parent; the child (dfx) still has it open
    os.close(slave_fd)

    # We'll accumulate everything the child prints in this list
    output_chunks = []

    try:
        # 3) Forward data between the user and the subprocess until the subprocess ends
        while True:
            # Use 'select' to wait for either the user typing something (sys.stdin)
            # or the subprocess producing output (master_fd)
            rlist, _, _ = select.select([master_fd, sys.stdin], [], [])

            # If the subprocess has output, read it and display on our terminal
            if master_fd in rlist:
                try:
                    data = os.read(master_fd, 1024)
                except OSError:
                    break

                if not data:
                    # EOF from the subprocess
                    break

                decoded = data.decode("utf-8", errors="replace")
                # Echo what the subprocess wrote to our terminal
                sys.stdout.write(decoded)
                sys.stdout.flush()
                # Also keep a copy so we can parse it later
                output_chunks.append(decoded)

            # If the user typed something in our terminal, send it to the subprocess
            if sys.stdin in rlist:
                user_input = sys.stdin.readline()
                if not user_input:
                    # EOF from user (Ctrl-D), just continue
                    continue
                # Forward user's keystrokes to the subprocess
                os.write(master_fd, user_input.encode("utf-8"))

        # 4) Wait for 'dfx identity new' to finish
        exit_code = process.wait()

    finally:
        # Make sure we close the master fd
        try:
            os.close(master_fd)
        except OSError:
            pass

    # 5) Combine all collected output into a single string
    final_output = "".join(output_chunks)

    # 6) Check the process exit code
    if exit_code != 0:
        print("Error: 'dfx identity new' returned a non-zero exit code.")
        return {"status": False}

    # 7) Extract the seed phrase from the final output using a regex
    #    Adjust this pattern if your DFX text differs
    seed_phrase_match = re.search(
        r"Your seed phrase for identity '[^']+': (.*)", 
        final_output
    )
    if seed_phrase_match:
        seed_phrase = seed_phrase_match.group(1).strip()
        print(f"\nSuccessfully created '{username}' with seed phrase:\n{seed_phrase}")
        return {"status": True, "seedPhrase": seed_phrase}
    else:
        print("No seed phrase found in the output.")
        return {"status": False}
