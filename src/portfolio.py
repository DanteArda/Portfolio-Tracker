import broker_response
from exception import *
from currency_symbols import CurrencySymbols

class Portfolio:
    """
    Class Representing the whole portfolio
    """
    api_key_map = dict()

    class Cash:
        """Class representing the portfolio value, and any free cash"""
        free = 0 # uninvested cash
        invested = 0 # invested cash (not including unrealized gains)
        ppl = 0 # profit or total of unrealized gains
        ppl_pc = 0 # percentage difference between invested and total
        result = 0 # realized gains
        total = 0 # entire portfolio value
        dividend_total = 0 # all the dividends
        last_dividend = 0
        currency_code = "USD"
        currency_symbol = "$"

    class Stock:
        """Class representing the stocks held"""
        total = 0 # all stocks value combined

    class Crypto:
        """Class representing any Crypto held via on an Exchange or Personal Wallet (if it has an API)"""
        total = 0 # all crypto coins value combined

    class History:
        """Class for storing any movements, """

    def auth_api(self, broker : str, api_key: str) -> bool:
        """
        Return if the API request returns a response, using the auth_api module from the Broker class

        :param broker: Broker's name
        :param api_key: The API key
        :returns: bool
        """
        instance = broker_response.get_class_from_str(broker, api_key)
        return instance.auth_api()
    
    def __precheck__(self):
        """Check if the api_key_map has been assigned and validated"""
        if self.api_key_map: return
        raise PrematureEvaluationError("api_key_map", self)
    
    @staticmethod
    def percentage_change(previous : int, current : int):
        """Return the percentage change in non-decimal unrounded form"""
        if previous == current: return 100
        try:
            return ((current - previous) / previous) * 100
        except:
            return 0

    def read(self):
        """Read all APIs and blend into Portfolio's attributes"""
        self.__precheck__()

        for Broker in self.api_key_map:
            match Broker:
                # Broker
                case "Trading212": self.__Trading212__()

                # Exchange
                

                # Other
                case _:
                    raise AttributeError(f"Portfolio object has no case for {Broker}")
                
        # end of blending summary
        self.Cash.ppl_pc = self.percentage_change(self.Cash.invested, self.Cash.total)

    def __Trading212__(self):
        """Blend Trading212 API into Portfolio's attributes"""
        self.__precheck__()
        Trading212 = broker_response.Trading212(self.api_key_map["Trading212"]["api_key"])

        # Account Data
        account_cash = Trading212.get_account_cash()
        """
        {
            "blocked": 0,
            "free": 0,
            "invested": 0,
            "pieCash": 0,
            "ppl": 0,
            "result": 0,
            "total": 0
        }
        """
        self.Cash.free += account_cash["free"]
        self.Cash.invested += account_cash["invested"]
        self.Cash.ppl = account_cash["ppl"]
        self.Cash.result = account_cash["result"]
        self.Cash.total = account_cash["total"]

        account_metadata = Trading212.get_account_metadata()
        """
        {
            "currencyCode": "USD",
            "id": 0
        }
        """
        self.Cash.currency_code = account_metadata["currencyCode"]
        self.Cash.currency_symbol = CurrencySymbols.get_symbol(self.Cash.currency_code)
        
        # Historical items
        paid_out_dividends = Trading212.get_paid_out_dividends()
        """
        {
            "items": [
                {
                "amount": 0,
                "amountInEuro": 0,
                "grossAmountPerShare": 0,
                "paidOn": "2019-08-24T14:15:22Z",
                "quantity": 0,
                "reference": "string",
                "ticker": "string",
                "type": "ORDINARY"
                }
            ],
            "nextPagePath": "string"
        }
        """
        for payment in paid_out_dividends['items']:
            self.Cash.dividend_total  += payment["amount"]
            self.Cash.last_dividend = payment["amount"]