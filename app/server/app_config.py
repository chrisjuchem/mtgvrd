class AppConfig:
    """
    Overrides to the default flask config
    """

    # This is the default for production but not for local dev; force them to match
    PROPAGATE_EXCEPTIONS = False


app_config = AppConfig()
