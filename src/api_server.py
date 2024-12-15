import api_service
from portfolio_generator import Portfolio
from abc import ABC, abstractmethod
from currency_symbols import CurrencySymbols

class _AbstractAPIService(ABC):
    cash_dict = Portfolio.filter_attributes(Portfolio.Cash)

    @abstractmethod
    def get_cash(self) -> "Portfolio":
        """Get numerical and liquid data about a Portfolio"""
        pass

class Trading212(_AbstractAPIService, api_service.Trading212):
    def get_cash(self):
        cash_dict = self.cash_dict.copy()

        fetch_account_cash = super().fetch_account_cash()
        """
        Response Sample:
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
        cash_dict['blocked'] = fetch_account_cash['blocked']
        cash_dict['free'] = fetch_account_cash['free']
        cash_dict['invested'] = fetch_account_cash['invested'] + fetch_account_cash['pieCash']
        cash_dict['profit_and_loss'] = fetch_account_cash['ppl']
        cash_dict['realized'] = fetch_account_cash['result']
        cash_dict['total'] = fetch_account_cash['total']

        fetch_account_metadata = super().fetch_account_metadata()
        """
        Response Sample:
            {
                "currencyCode": "USD",
                "id": 0
            }
        """
        cash_dict['currency_metadata'] = CurrencySymbols.get_symbol(fetch_account_metadata['currencyCode'])

        paid_out_dividends = super().paid_out_dividends()
        """
        Response Sample:
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
                      "type": "string"
                    }
                ],
                "nextPagePath": "string"
            }
        """
        total_dividend = 0
        for dividend_payment in paid_out_dividends['items']:
            total_dividend += dividend_payment['amount']
        cash_dict['total_dividend'] = total_dividend

        return cash_dict


