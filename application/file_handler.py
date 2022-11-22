import os
import sys

class FileManager():
    """
    Class to manage files, handling errors, adding cross platform support.

    Args:
        None

    Attributes:
        cwd (str): Current working directory for file naviation
    """

    def __init__(self):
        self.cwd = os.getcwd()

    def create_path_string(self, *args: str) -> str:
        """
        Safely convert inputs into a path string, ensuring formatting
        isn't an issue across different OS

        Args:
            *args (strs): collection of strings to be combined for a directory/file path

        Returns:
            final_path (str): string for new directory building from the current working directory
        """
        final_path = self.cwd

        for child in args:
            final_path = os.path.join(final_path, child)

        return final_path

    def exists(self, path: str) -> bool:
        """
        Return a boolean on whether a file/directory exists

        Args:
            path (str): path to be tested

        Returns:
            True/False (bool): boolean response to if the file/directory exists
        """
        return os.path.exists(path)

    def load_file(self):
        pass

    def make_file(self):
        pass

    def delete_file(self):
        pass

    def save(self, data, location: str, file_extension: str) -> None:
        pass


if __name__ == "__main__":
    fm = FileManager()
    