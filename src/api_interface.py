import api_service
from portfolio_generator import Portfolio

class Hook:
    """A bridge between a Platform's API methods and the local portfolio"""
    Observer = Observer()

    def __init__(self, broker_api : "api_service", portfolio : "Portfolio"):
        self.broker_api = broker_api
        self.portfolio = portfolio 

    def write_cash(self):
        """Read and Write from broker api to the Portfolio class."""
        cash_dict = Portfolio.filter_attributes(Portfolio.Cash())

        # TODO
        # write from api to cash_dict

        self.portfolio.write_to(self.portfolio.Cash, cash_dict)

class Observer:
    """A class to observe the hook, and return a progress report"""
