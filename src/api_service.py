import requests

class Trading212:
    """Class for the Broker Trading212\n
    http://trading212.com"""
    base_url = "https://live.trading212.com"

    def __init__(self, API_key):
        self.API_key = API_key

    # Account Data
    def fetch_account_cash(self):
        """Fetch all account balances."""
        return self.request("GET", "/api/v0/equity/account/cash")
    
    def fetch_account_metadata(self):
        """Fetch all account information."""
        return self.request("GET", "/api/v0/equity/account/info")
    
    # Personal Portfolio
    def fetch_all_open_positions(self):
        """Fetch all open positions."""
        return self.request("GET", "/api/v0/equity/portfolio")
    
    def search_for_a_specific_position_by_ticker(self, ticker):
        """Search for an open position by ticker."""
        return self.request("POST", "/api/v0/equity/portfolio/ticker", ticker)
    
    def fetch_a_specifc_position(self, ticker : str):
        """Fetch an open position by ticker."""
        return self.request("GET", f"/api/v0/equity/portfolio/{ticker}")

    # API
    def request(self, method : str, path : str, body : str) -> dict:
        """
        Request data from an API endpoint.
    
        Args:
            method (str): Whether to send a GET or POST request.
            path (str): path to the API endpoint.
            body (str): additional parameters to be sent.

        Returns:
            dict: json object with request data, or nothing if an error.
        """
        url = self.base_url + path

        headers = {
            "Content-Type": "application/json",
            "Authorization" : self.API_key
            }

        if method == "GET":
            response = requests.get(url, headers=headers)

        elif method == "POST":
            payload = {
                "ticker" : body
            }

            response = requests.post(url, json=payload, headers=headers)

        else:
            pass

        return response.json()