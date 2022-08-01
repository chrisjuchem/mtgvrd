import json
import os


class ConfigManager:
    def __init__(self):
        secrets_file = os.environ.get("SECRETS_FILE", "app/server/secrets.json")

        if os.path.isfile(secrets_file):
            with open(secrets_file, "r", encoding="utf8") as file:
                self.secrets = json.load(file)
        else:
            self.secrets = {}

    def __getitem__(self, key):
        if key in self.secrets:
            return self.secrets[key]
        return os.environ[key]


config = ConfigManager()


# ===================================================


class AppConfig:
    """
    Overrides to the default flask config
    """

    # This is the default for production but not for local dev; force them to match
    PROPAGATE_EXCEPTIONS = False

    SECRET_KEY = config["FLASK_SECRET_KEY"]


app_config = AppConfig()
