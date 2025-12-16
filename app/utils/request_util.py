import requests

class RequestUtil:
    @staticmethod
    def send_get_request(url: str, params: dict, headers: dict) -> requests.Response:
        """Send a GET request to the specified URL with optional parameters and headers."""
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"An error occurred while making GET request to {url}: {e}")
            raise