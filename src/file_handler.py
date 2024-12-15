import os
import configparser
import json
import time

class Config:
    """An Interface for permanent non-volatile data."""

    class Ini:
        """For dealing with .ini config files.\n
        Currently only API keys for each platform is being saved."""
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

        def get_all(self) -> list:
            """
            Get all the platforms that have been saved.

            Returns:
                list: A list of platforms that have been saved.
            """
            return self.ini_config.sections()

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

        def load(self) -> dict:
            """
            Load the API keys into a dictionary.

            Returns:
                dict: The API keys.
            """
            keys = {}
            for platform in self.get_all():
                keys[platform] = self.get(platform)

            return keys

    class Json:
        """For dealing with .json config files."""

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        local_dir = os.path.join(cur_dir, "local")

        json_file_dir = os.path.join(local_dir, "trading212.json")

        def __init__(self):
            if not os.path.isdir(self.local_dir):
                # Dir doesn't exist
                os.makedirs(self.local_dir)

        def has_platform(self, platform : str) -> bool:
            """
            Checks if data exists for a trading platform.

            Args:
                platform (str): The trading platform to search for.

            Returns:
                bool: True if the data exists, False otherwise.
            """
            return platform in self.load()

        def get(self, platform :str) -> dict:
            """
            Return the portfolio data for a platform.

            Args:
                platform (str): The trading platform to search for.

            Returns:
                dict: The portfolio data.
            """
            return self.load()[platform]

        def save(self, data : dict, platform: str):
            """
            Save dict to disk.

            Args:
                data (dict): The data to save.
                platform (str): The trading platform the data belongs to.
            """
            data['generated'] = time.time()

            disk_data = self.load()
            disk_data[platform] = data

            with open(self.json_file_dir, 'w') as json_file:
                json.dump(disk_data, json_file, indent=4)

        def load(self) -> dict:
            """
            Load dict from disk.

            Returns:
                dict: The data loaded from the json file.
            """
            if not self.is_empty():
                with open(self.json_file_dir, 'r') as json_file:
                    return json.load(json_file)
            return {}

        def is_empty(self) -> bool:
            """
            Checks if the file is empty.

            Returns:
                bool: True if the file is empty, False otherwise.
            """
            if os.path.getsize(self.json_file_dir) == 0:
                return True

            try:
                with open(self.json_file_dir, "r") as file:
                    content = file.read().strip()
                    if not content:  # Completely empty content
                        return True

                    data = json.loads(content)

                    return data != {} or data != []

            except json.JSONDecodeError:
                return False

        def is_outdated(self, platform : str) -> bool:
            """
            Checks if the 'generated' value is outdated.

            Args:
                platform (str): The trading platform the data belongs to.

            Returns:
                bool: True if the data is outdated, False otherwise.
            """
            # The time the data can be fresh before it must be overwritten.
            OUTDATED_THRESHOLD = 15 * 60

            if self.is_empty(): return True # No generated value

            data_birth = self.get(platform).get('generated')
            return time.time() > data_birth + OUTDATED_THRESHOLD