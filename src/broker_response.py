import requests
from exception import *

DEFAULT_QUERY = {
    "cursor": None,
    "ticker": None,
    "limit": 50,
}

DEFAULT_PAYLOAD = {
    "Export csv": {
        "dataIncluded": {
            "includeDividends": False,
            "includeInterest": False,
            "includeOrders": True,
            "includeTransactions": False
        },
        "timeFrom": 0,
        "timeTo": 0
    }
}

def get_class_from_str(name : str, *args, **kwargs):
    """
    Get any class instace from broker_response

    :param name: The name of the class instance
    :param *args: If the class requires an init variable
    :returns: an Instance of the class
    """
    cls = globals().get(name)
    if cls is None: raise ValueError(f"Class {name} not found")

    return cls(*args, **kwargs)

class Broker:
    """
    Class that represents a Financial Broker
    """
    def __init__(self, api_key):
        self.api_key = api_key

    # Abstract Method
    def auth_api(self) -> bool:
        """
        Does a quick request to validate an API key

        Recommended by checking that a status code of 200 is returned

        This is an abstract method, it should be modified to suit each Broker's API

        :returns: bool stating whether the API is valid or not (assuming 401 is the only instance where API is bad)
        """
        raise NotImplementedError(f"'{self.__class__.__name__}' must impliment the abstract 'auth_api' method")

    # Websocket
    def post_response(self, url : str, payload : dict):
        """
        Sends a request to perform an action from url

        :param url: Where the payload is sent to
        :param payload: The request body schema
        :returns: json parsed as dict
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200: raise BadStatusCodeError(response.status_code)
        return response.json()

    def get_response(self, url : str, query : dict = None) -> dict | BadStatusCodeError:
        """
        Sends a request to retrieve data from url

        :param url: Where the request is sent to
        :param query: any additional parameters required
        :returns: json parsed as dict
        """

        headers = {"Authorization": self.api_key}

        response = requests.get(url, headers=headers, params=query)

        if response.status_code != 200: raise BadStatusCodeError(response.status_code)
        return response.json()

class Trading212(Broker):
    """
    Class to handle responses from Trading212

    Trading212: https://www.trading212.com/\n
    Trading212 API Docs: https://t212public-api-docs.redoc.ly/
    """
    def __init__(self, api_key):
        super().__init__(api_key)

    def auth_api(self) -> bool:
        try:
            self.get_account_cash()
        except BadStatusCodeError as Response:
            status_code = Response.status_code

            return status_code != 401
        return True

    # Instruments Metadata

    # Pies

    # Equity Orders

    # Account Data
    def get_account_cash(self):
        """Fetch all information about available cash, interpolated cash and portfolio value"""
        return super().get_response("https://live.trading212.com/api/v0/equity/account/cash")
    
    def get_account_metadata(self):
        """Fetch customer account currency"""
        return super().get_response("https://live.trading212.com/api/v0/equity/account/info")

    # Personal Portfolio
    def get_all_open_positions(self):
        """Fetch all open positions for your account"""
        return super().get_response("https://live.trading212.com/api/v0/equity/portfolio")
    
    def get_a_specific_position(self, ticker : str):
        """Fetch an open position by ticker otherwise just fetch all"""
        url = "https://live.trading212.com/api/v0/equity/portfolio"
        if ticker: url += f"/{ticker}"

        return super().get_response(url)
    
    # Historical items
    def get_historical_order_data(self, query : dict = DEFAULT_QUERY):
        """Get all order history"""
        return super().get_response("https://live.trading212.com/api/v0/equity/history/orders", query)
    
    def get_paid_out_dividends(self, query : dict = DEFAULT_QUERY):
        """Get all dividend history"""
        return super().get_response("https://live.trading212.com/api/v0/history/dividends", query)
    
    def get_exports_list(self):
        """Lists detailed information about all csv account exports"""
        return super().get_response("https://live.trading212.com/api/v0/history/exports")
    
    def post_export_csv(self, payload : dict = DEFAULT_PAYLOAD["Export csv"]):
        """Request a csv export of the account's orders, dividends and transactions history"""
        return super().post_response("https://live.trading212.com/api/v0/history/exports", payload)
    
    def get_transaction_list(self, query : dict = DEFAULT_QUERY):
        """Fetch superficial information about movements to and from your account"""
        return super().get_response("https://live.trading212.com/api/v0/history/transactions", query)