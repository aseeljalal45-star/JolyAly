import json, os

class SettingsManager:
    def __init__(self, config_file="config/config.json"):
        self.config_file = config_file
        self.settings = self.load_settings()

    def load_settings(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"language": "ar", "theme": "light"}

    def save_settings(self):
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, ensure_ascii=False, indent=2)

    def set(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def get(self, key, default=None):
        return self.settings.get(key, default)