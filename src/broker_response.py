import requests

class Broker:
    """
    Class that represents a Financial Broker
    """
    def __init__(self, apiKey):
        self.apiKey = apiKey

class Trading212(Broker):
    """
    Class to handle responses from Trading212

    Trading212: https://www.trading212.com/\n
    Trading212 API Docs: https://t212public-api-docs.redoc.ly/
    """
    def __init__(self, apiKey):
        super().__init__(apiKey)

        