import api_service
import portfolio_generator

class Hook:
    def __init__(self, broker_api : api_service, portfolio : portfolio_generator.Portfolio):
        self.broker_api = broker_api
        self.portfolio = portfolio 

    
    

