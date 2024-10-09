import requests

EMPTY_QUERY = {
        "cursor": None,
        "ticker": None,
        "limit": 50
    }

class Builder:
    def __init__(self, apiKey):
        self.__apiKey__ = apiKey

    # Account Data
    def get_account_cash(self):
        return self.get_response("https://live.trading212.com/api/v0/equity/account/cash")
    
    def get_account_metadata(self):
        return self.get_response("https://live.trading212.com/api/v0/equity/account/info")

    # Personal Portfolio
    def get_all_open_positions(self):
        return self.get_response("https://live.trading212.com/api/v0/equity/portfolio")
    
    def get_a_specific_position(self, ticker : str):
        return self.get_response("https://live.trading212.com/api/v0/equity/portfolio/" + ticker)
    
    # Historical Items
    def get_historical_order_data(self, query : dict = EMPTY_QUERY):
        return self.get_response("https://live.trading212.com/api/v0/equity/history/orders", query)
    
    def get_paid_out_dividends(self, query : dict = EMPTY_QUERY):
        return self.get_response("https://live.trading212.com/api/v0/history/dividends", query)
    
    def get_export_list(self):
        return self.get_response("https://live.trading212.com/api/v0/history/exports")

    # Web Socket
    def get_response(self, url : str, params : dict = None) -> dict:

        headers = {"Authorization": self.__apiKey__}

        response = requests.get(url, headers=headers, params=params)

        return response.json() if response.status_code == 200 else response.status_code