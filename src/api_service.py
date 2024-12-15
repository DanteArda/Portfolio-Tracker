import requests

class Trading212:
    """Class for the Broker Trading212\n
    http://trading212.com"""
    base_url = "https://live.trading212.com"

    DEFAULT_QUERY_PARAMETERS = {
        "cursor" : "0",
        "ticker" : None,
        "limit" : 50
    }

    DEFAULT_TRANSACTION_QUERY_PARAMETERS = {
        "cursor" : "0",
        "time" : "2000-01-01 00:00:00",
        "limit" : 50
    }

    DEFAULT_BODY_SCHEMA = {
        "dataIncluded" : {
            "includeDividends" : True,
            "includeInterest" : True,
            "includeOrders" : True,
            "includeTransactions" : True 
        },
        "timeFrom" : "2000-01-01 00:00:00",
        "timeTo" : "3000-01-01 00:00:00"
    }

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
        body = {"ticker" : ticker}
        return self.request("POST", "/api/v0/equity/portfolio/ticker", body)
    
    def fetch_a_specifc_position(self, ticker : str):
        """Fetch an open position by ticker."""
        return self.request("GET", f"/api/v0/equity/portfolio/{ticker}")

    # Historical Items
    def historical_order_data(self, query : dict = DEFAULT_QUERY_PARAMETERS):
        """Fetch all historical order data for positions."""
        return self.request("GET", "/api/v0/equity/history/orders", query)

    def paid_out_dividends(self, query : dict = DEFAULT_QUERY_PARAMETERS):
        """Fetch all historical dividend payments."""
        return self.request("GET", "/api/v0/history/dividends", query)

    def exports_list(self):
        """List detailed information about all csv account exports."""
        return self.request("GET", "/api/v0/history/exports")

    def export_csv(self, query : dict = DEFAULT_QUERY_PARAMETERS):
        """Request a csv export of the account's orders, dividends and transactions history"""
        return self.request("POST", "/api/v0/history/exports", query)

    def transaction_list(self, query : dict = DEFAULT_TRANSACTION_QUERY_PARAMETERS):
        """Return monetary movements in and out of the account"""
        return self.request("GET", "/api/v0/history/transactions", query)

    # API
    def request(self, method : str, path : str, body : dict = None) -> dict:
        """
        Request data from an API endpoint.
    
        Args:
            method (str): Whether to send a GET or POST request.
            path (str): path to the API endpoint.
            body (dict): additional parameters to be sent.

        Returns:
            dict: json object with request data, or nothing if an error.
        """
        url = self.base_url + path

        headers = {
            "Content-Type": "application/json",
            "Authorization" : self.API_key
            }

        if method == "GET":
            response = requests.get(url, headers=headers, params=body)

        elif method == "POST":
            response = requests.post(url, json=body, headers=headers)

        else:
            pass

        if response.status_code == 200: return response.json()
        return {}