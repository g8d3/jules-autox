import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Application configuration settings.
    Loads values from environment variables, with defaults.
    """
    # Browser settings
    HEADLESS_MODE: bool = os.getenv('HEADLESS_MODE', 'True').lower() == 'true'

    # Timing settings
    DEFAULT_WAIT_TIME: int = int(os.getenv('DEFAULT_WAIT_TIME', '5000')) # in milliseconds

    # Add more configuration variables as needed

# Instantiate the config object for easy access
app_config = Config()

if __name__ == '__main__':
    # For testing purposes, print the loaded config
    print(f"Headless Mode: {app_config.HEADLESS_MODE} (Type: {type(app_config.HEADLESS_MODE)})")
    print(f"Default Wait Time: {app_config.DEFAULT_WAIT_TIME} (Type: {type(app_config.DEFAULT_WAIT_TIME)})")
