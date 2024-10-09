import pandas
import builder

class Portfolio:
    class Cash:
        blocked = 0
        free = 0
        invested = 0
        pieCash = 0
        ppl = 0
        ppl_pc = 0
        result = 0
        total = 0
        dividend_total = 0

    class Stock:
        pass

    class History:
        export_list_csv = None
        portfolio_history_dataframe = None

        def convert_csv_to_dataframe(self, pathfile):
            self.portfolio_history_dataframe = pandas.read_csv(pathfile)

    def read(self, apiKey):
        Trading212 = builder.Builder(apiKey)

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
        for key, value in account_cash:
            if hasattr(self.Cash, key): 
                setattr(self.Cash, key, value)
        self.Cash.ppl_pc = percentage_change(self.Cash.invested, self.Cash.total)

        # Historical Items
        dividends = Trading212.get_paid_out_dividends()
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
        for payment in dividends["items"]:
            self.Cash.dividend_total += payment["amount"]

        exports_list = Trading212.get_export_list()
        """
        [
            {
                "dataIncluded": {
                "includeDividends": true,
                "includeInterest": true,
                "includeOrders": true,
                "includeTransactions": true
                },
                "downloadLink": "string",
                "reportId": 0,
                "status": "Queued",
                "timeFrom": "2019-08-24T14:15:22Z",
                "timeTo": "2019-08-24T14:15:22Z"
            }
        ]
        """
        self.History.export_list_csv = exports_list

def percentage_change(prev_val : int, cur_val : int):
    return ( (cur_val - prev_val) / prev_val ) * 100 