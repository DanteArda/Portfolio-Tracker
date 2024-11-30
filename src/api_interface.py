import api_service
from portfolio_generator import Portfolio

class Hook:
    def __init__(self, broker_api : "api_service", portfolio : "Portfolio"):
        self.broker_api = broker_api
        self.portfolio = portfolio 

    def write_cash(self):
        """Read and Write from broker api to the Portfolio class."""
        cash_dict = Portfolio.filter_new_cash_attributes()

        # TODO
        # write from api to cash_dict

        self.portfolio.write_to(self.portfolio.Cash, cash_dict)
        
