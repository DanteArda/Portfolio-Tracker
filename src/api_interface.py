import api_server
from portfolio_generator import Portfolio

class Observer:
    """A class to observe the hook, and return a progress report"""
    state = "Inactive"

class Hook:
    """A bridge between a Platform's API methods and the local portfolio"""
    observer = Observer()

    def __init__(self, platform : "api_server", portfolio : "Portfolio"):
        self.platform = platform
        self.portfolio = portfolio 

    def write_cash(self):
        """Read and Write from broker api to the Portfolio class."""
        cash_dict = self.platform.get_cash()

        self.portfolio.write_to(self.portfolio.Cash, cash_dict)
