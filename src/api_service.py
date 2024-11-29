import requests

class Trading212:
    """Class for the Broker Trading212\n
    http://trading212.com"""
    base_url = "https://live.trading212.com"

    def __init__(self, API_key):
        self.API_key = API_key

    # Account Data
    def fetch_account_cash(self):
        return self.request("GET", "/api/v0/equity/account/cash")

    # API
    def request(self, method, path) -> dict:
        """
        Request data from an API endpoint.
    
        Args:
            method (str): Whether to send a GET or POST request.
            path (str): path to the API endpoint.

        Returns:
            dict: json object with request data, or nothing if an error.
        """
        url = self.base_url + path

        headers = {"Authorization" : self.API_key}

        if method == "GET":
            response = requests.get(url, headers=headers)

        elif method == "POST":
            pass

        else:
            pass

        return response.json()