import os
import configparser

class ConfigAPI:
    """An Interface for making it incredibly easy to read and write from a .ini config file."""

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    local_dir = os.path.join(cur_dir, "local")
    config_file_dir = os.path.join(local_dir, "config.ini")

    config = configparser.ConfigParser()

    def __init__(self):
        if os.path.isdir(self.local_dir) and os.path.exists(self.config_file_dir):
            # File exists
            self.config.read(self.config_file_dir)

        else:
            # File or directory doesn't exist
            os.makedirs(self.local_dir)
            with open(self.config_file_dir, 'w'): pass

    def set(self, platform : str, value : str, option : str = "API_key"):
        """
        Set the key associated to the platform.

        Args:
            platform (str): The trading platfrom the key belongs to.
            value (str): The key value.
            option (str): The key name, default is "API_key".
        """
        if not self.has_platform(platform):
            self.config.add_section(platform)
        
        self.config.set(platform, option, value)

    def has_platform(self, platform : str):
        """
        Check if a section exists for a trading platform.

        Args:
            section (str): The section name to check.

        Returns:
            bool: True if the section is found, False otherwise.
        """
        return self.config.has_section(platform)

    def save(self):
        """Save the configuration to a file."""
        with open(self.config_file_dir, 'w') as config_file:
            self.config.write(config_file)

    