import os
import shutil

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
            (bool): boolean response to if the file/directory exists
        """
        return os.path.exists(path)

    def make_file(self, path: str, file_exstension: str) -> bool:
        """
        Provided a file doesn't already exist, create it
        Otherwise, notify that the file already exists

        Args:
            path (str): path to the file to be created
            file_exstension(str): exstention of the file to be deleted, e.g., .py, .txt

        Returns:
            (bool): True or False depending on the success of the creation of a file
        """
        completed_path = path + file_exstension

        if not self.exists(completed_path):
            open(completed_path, 'w', encoding='utf-8').close()
            return True

        print(f"Sorry, file {completed_path} already exists.")

        return False

    def make_directory(self, path: str) -> bool:
        """
        Provided a directory doesn't exist, create the directory
        Otherwise, notify that the directory already exists

        Args:
            path (str): path for the directory desired to be created

        Returns:
            (bool): True or False dependonf on the success on the creation of a directory
        """
        if not self.exists(path):
            os.mkdir(path)
            return True

        print(f"Sorry, directory {path} already exists.")

        return False

    def delete_file(self, path: str) -> bool:
        """
        Provided a file exists, remove it, otherwise notify that the file
        doesn't exist in the first place

        Args:
            path (str): Path for the file to be deleted

        Returns:
            (bool): True or False depending on the success of deletion
        """
        if self.exists(path):
            os.remove(path)
            return True

        print(f"Sorry, {path} doesn't exist, cannot be deleted.")

        return False

    def delete_directory(self, path: str) -> bool:
        """
        Provided a directory exists, remove it, otherwise notify that the file
        doesn't exist in the first place

        Args:
            path (str): Path for the file to be deleted

        Returns:
            (bool): True or False depending on the success of deletion
        """

        if self.exists(path):
            shutil.rmtree(path)
            return True

        print(f"Sorry, {path} doesn't exist, cannot be deleted")

        return False

    def items_in_directory(self, location: str) -> list:
        if self.exists(location):
            return os.listdir(location)
        
        print(f"Sorry, {location} doesn't exist.")
        return []

    def save_file(self, data, location: str, file_extension: str, mode: str) -> None:
        pass


if __name__ == "__main__":
    fm = FileManager()
