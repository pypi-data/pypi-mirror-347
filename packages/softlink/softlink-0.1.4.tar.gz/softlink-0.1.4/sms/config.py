import os
from typing import Optional


class SMSConfig:
    """
    Configuration class for Softlink SMS API integration.

    This class handles configuration settings for connecting to the Softlink SMS API,
    including authentication credentials and environment settings.

    Args:
        consumer_key (Optional[str]): The API key for authentication.
            Defaults to SOFTLINK_SMS_API_KEY environment variable if not provided.

    Attributes:
        consumer_key (str): The API key used for authentication
        production_url (str): The production API base URL
        headers (Dict[str, str]): Request headers including authentication
    """

    def __init__(self, consumer_key: Optional[str] = None):
        self.consumer_key = consumer_key or os.getenv("SOFTLINK_SMS_API_KEY")
        self.production_url = "https://api.softlinksms.co.ke"
        self.headers = {"Authorization": f"Basic {self.consumer_key}"}
