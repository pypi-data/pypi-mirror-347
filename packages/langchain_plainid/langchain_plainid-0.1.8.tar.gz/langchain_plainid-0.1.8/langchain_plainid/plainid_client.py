import json
import logging
from typing import Any, Dict, Optional

import requests

# Configure module logger
logger = logging.getLogger(__name__)


class PlainIDClient:
    def __init__(
        self, base_url: str, client_id: str, client_secret: str, entity_type_id: str
    ):
        """
        Initialize PlainIDClient with authentication credentials.

        Args:
            base_url (str): Base URL for PlainID service
            client_id (str): Client ID for authentication
            client_secret (str): Client secret for authentication
            entity_type_id (str): Entity type ID for the request
        """
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.entity_type_id = entity_type_id

    def get_resolution(
        self, entity_id: str, include_attributes: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Gets resolution data from PlainID API.

        Args:
            entity_id (str): The entity ID to get resolution for
            include_attributes (bool): Whether to include attributes in the response

        Returns:
            Optional[Dict[str, Any]]: Resolution data from PlainID or None if there was an error
        """
        try:
            logger.debug("getting resolution... %s", entity_id)
            headers = {
                "Content-Type": "application/json",
            }

            payload = {
                "clientId": self.client_id,
                "clientSecret": self.client_secret,
                "entityId": entity_id,
                "entityTypeId": self.entity_type_id,
                "includeAttributes": include_attributes,
            }

            logging.debug("payload: %s", payload)
            response = requests.post(
                f"{self.base_url}/runtime/resolution/v3",
                headers=headers,
                data=json.dumps(payload),
            )
            response.raise_for_status()
            resolution = response.json()
            logger.debug("resolution: %s", resolution)

            return resolution
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching PlainID resolution: %s", str(e))
            return None

    def get_token(
        self, entity_id: str = "user", include_attributes: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Gets token data from PlainID API.

        Args:
            entity_id (str): The entity ID to get resolution for
            include_attributes (bool): Whether to include attributes in the response

        Returns:
            Optional[Dict[str, Any]]: Topic data from PlainID or None if there was an error
        """
        try:
            headers = {
                "Content-Type": "application/json",
            }
            payload = {
                "clientId": self.client_id,
                "clientSecret": self.client_secret,
                "entityId": entity_id,
                "includeAttributes": include_attributes,
            }

            logger.debug("payload: %s", payload)

            response = requests.post(
                f"{self.base_url}/runtime/token/v3",
                headers=headers,
                data=json.dumps(payload),
            )

            logger.debug("plaind id client response : %s", response.json())

            response.raise_for_status()
            resolution = response.json()
            logger.debug("token: %s", resolution)

            return resolution
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching PlainID token: %s", str(e))
            return None
