import os
import configparser
import json

class Config:
    """An Interface for making it incredibly easy to read and write from a .ini config file."""

    class Ini:
        """For dealing with .ini config files."""
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        local_dir = os.path.join(cur_dir, "local")

        ini_file_dir = os.path.join(local_dir, "config.ini")
        ini_config = configparser.ConfigParser()

        def __init__(self):
            if os.path.isdir(self.local_dir) and os.path.exists(self.ini_file_dir):
                # File exists
                self.ini_config.read(self.ini_file_dir)

            else:
                # File or directory doesn't exist
                os.makedirs(self.local_dir)
                with open(self.ini_file_dir, 'w'): pass

        def set(self, platform : str, value : str, name : str = "API_key"):
            """
            Set the key associated to the platform.

            Args:
                platform (str): The trading platform the key belongs to.
                value (str): The key value.
                name (str): The key name, default is "API_key".
            """
            if not self.has_platform(platform):
                self.ini_config.add_section(platform)

            self.ini_config.set(platform, name, value)

        def get(self, platform : str, fetch : str = "API_key") -> str:
            """
            Get the key for a specified trading platform.

            Args:
                platform (str): The trading platform to search for.
                fetch (str): The specified key name, default is 'API_KEY'

            Returns:
                str: The API key, nothing if not found.
            """
            return self.ini_config.get(platform, fetch)

        def has_platform(self, platform : str):
            """
            Check if a section exists for a trading platform.

            Args:
                platform (str): The section name to check.

            Returns:
                bool: True if the section is found, False otherwise.
            """
            return self.ini_config.has_section(platform)

        def save(self):
            """Save the configuration to a file."""
            with open(self.ini_file_dir, 'w') as config_file:
                self.ini_config.write(config_file)

        class Json:
            """For dealing with .json config files."""