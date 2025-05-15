import json
import requests
from typing import Optional

class Rholambda:
    _api_key: Optional[str] = None
    _base_url: str = 'https://api.rholambda.ai/api/v1'  # Replace with your actual base URL

    @classmethod
    def set_apk(cls, api_key: str) -> None:
        """Set the API key using set_apk (alternate to init)."""
        cls._api_key = api_key

    # @classmethod
    # def set_base_url(cls, base_url: str) -> None:
    #     """Optional: Configure custom base URL (useful for testing/staging environments)."""
    #     cls._base_url = base_url

    @classmethod
    def ask(cls, query: str) -> str:
        """Asks a question to the AI model on the Rholambda server.
        
        Args:
            query: The question to ask the AI model
            
        Returns:
            The response from the AI model
            
        Raises:
            Exception: If API key is not set or if the request fails
        """
        if cls._api_key is None:
            raise Exception('Rholambda API key not set. Use Rholambda.set_apk(your_api_key).')

        url = f"{cls._base_url}/ask"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {cls._api_key}'
        }
        data = {'query': query}

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            body = response.json()
            return body.get('response', '')
        else:
            raise Exception(f'Failed to get response: {response.status_code} {response.text}')