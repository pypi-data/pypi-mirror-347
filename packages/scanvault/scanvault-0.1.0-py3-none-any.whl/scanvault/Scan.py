import httpx
from ._config import get_api_url

class Scan:
    def __init__(self, token: str):
        """
        Initializes the Scan class with the provided API token.

        Args:
            token (str): The API token used for authentication.

        Attributes:
            base_url (str): The base URL for the API, retrieved using the `get_api_url` function.
            headers (dict): A dictionary containing the authorization header with the provided token.
        """
        self.base_url = get_api_url()
        self.headers = {'Authorization': f'Bearer {token}'}

    def scan(self, file_path: str) -> dict:
        """
        Scans a file by sending it to a remote scanning service.

        Args:
            file_path (str): The path to the file to be scanned.

        Returns:
            dict: A dictionary containing the response from the scanning service.
                  If an error occurs during the request, a dictionary with an "error" key
                  and the error message as its value is returned.

        Raises:
            httpx.RequestError: If there is an issue with the HTTP request.
        """
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (file_path, file)}
                response = httpx.post(f"{self.base_url}/scan/", headers=self.headers, files=files)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            return {"error": str(e)}