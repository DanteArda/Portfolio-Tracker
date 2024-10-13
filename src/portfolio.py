import broker_response

class Portfolio:
    """
    Class Representing the whole portfolio
    """
    class Cash:
        """Class representing the portfolio value, and any free cash"""

    class Stock:
        """Class representing the stocks held"""

    class Crypto:
        """Class representing any Crypto held via on an Exchange or Personal Wallet (if it has an API)"""

    def auth_api(self, broker : str, api_key: str) -> bool:
        """
        Return if the API request returns a response, using the auth_api module from the Broker class

        :param broker: Broker's name
        :param api_key: The API key
        :returns: bool
        """
        instance = broker_response.get_class_from_str(broker, api_key)
        return instance.auth_api()

    