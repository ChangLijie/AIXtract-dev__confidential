import subprocess
from typing import List


def split_command(command: str) -> List[str]:
    """
    Splits a command string into a list of arguments.
    Args:
        command (str): The command string to split.
    Returns:
        List[str]: A list of arguments.
    """
    try:
        return command.split()
    except Exception as e:
        raise ValueError(f"Error splitting command: {command}. Error: {e}")


def run_shell_command(command: str) -> str:
    """
    Runs a shell command.
    Args:
        command (str): The shell command to run.
    Returns:
        str: The output of the command.
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status.
    """
    # Split the command into a list of arguments

    args = split_command(command)

    # Use subprocess to run the command
    result = subprocess.run(args, check=True, capture_output=True, text=True)

    # For demonstration purposes, we will just print the command
    print(f"Running command: {args}")
    print(result.stdout)


if __name__ == "__main__":
    command = "ls -l"
    print(split_command(command))
    print(run_shell_command(command))
