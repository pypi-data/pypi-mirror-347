import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, "default_config.json")


class ConfigManager:
    """
    Handles loading, accessing, modifying, and saving configuration settings
    from a JSON file. Provides a simple interface to query and update config values.
    """

    def __init__(self, path=DEFAULT_CONFIG_PATH):
        self.path = path
        self.config = {}
        self.load()

    def load(self):
        """Load configuration from JSON file or create defaults if not found."""
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.config = json.load(f)
        else:
            print("No file config.json")

    def save(self):
        """Save the current configuration to the JSON file."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.config, f, indent=4)

    def get(self, section, key, default=None):
        """Get a configuration value by section and key."""
        return self.config.get(section, {}).get(key, default)

    def set(self, section, key, value):
        """Set a configuration value and persist it to disk."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
        self.save()
