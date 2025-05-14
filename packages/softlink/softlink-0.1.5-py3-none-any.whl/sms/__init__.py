from typing import Any, Dict, List, Optional

import requests

from .config import SMSConfig


class SMSClient:
    """
    Client class for interacting with the Softlink SMS API.

    This class provides methods for sending SMS messages through the Softlink SMS gateway.
    """

    def __init__(self, config: Optional[SMSConfig] = None):
        """
        Initialize the SMS client with configuration.

        Args:
            config: Optional SMSConfig instance. If not provided, default config will be used.
        """
        self.config = config or SMSConfig()

    def send_sms(self, message: str, recipients: List[str]) -> Dict[str, Any]:
        """
        Send an SMS message to one or more recipients.

        Sends a text message to the specified phone numbers using the Softlink SMS gateway API.
        The message will be delivered to all recipients in the provided list.

        Args:
            message (str): The message text to send
            recipients (List[str]): List of recipient phone numbers in international format
                (e.g. "+254713164545")

        Returns:
            Dict[str, Any]: Response from the API containing delivery status and details

        Raises:
            requests.exceptions.RequestException: If the API request fails
            requests.exceptions.Timeout: If the request times out after 30 seconds

        Example:
            >>> sms = SMSClient()
            >>> result = sms.send_sms(
            ...     message="Your verification code is 12345",
            ...     recipients=["+254712345678", "+254787654321"]
            ... )
        """
        return requests.post(
            f"{self.config.production_url}/api-messaging",
            headers=self.config.headers,
            json={"message": message, "recipients": recipients},
            timeout=30,
        )
