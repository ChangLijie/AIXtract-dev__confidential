import subprocess
from typing import List


class CommandLineExecutor:
    def _split_command(self, command: str) -> List[str]:
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

    def run(self, command: str) -> str:
        """
        Runs a shell command and returns the output.
        Args:
            command (str): The command to run.

        Returns:
            str: The output of the command.
        Raises:
            ValueError: If the command cannot be split or run.
        Raises:
            subprocess.CalledProcessError: If the command returns a non-zero exit status.
        """
        try:
            # Split the command into a list of arguments
            args = self._split_command(command)

            # Use subprocess to run the command
            result = subprocess.run(args, check=True, capture_output=True, text=True)

            # Return the output
            return result.stdout
        except ValueError as ve:
            raise ve
        except subprocess.CalledProcessError as cpe:
            raise ValueError(
                f"Command '{command}' failed with error: {cpe.stderr.strip()}"
            )


if __name__ == "__main__":
    command = "ls -l"
    commandline_executor = CommandLineExecutor()
    print(commandline_executor.run(command))
