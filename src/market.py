import pandas
import yfinance

class Market:
    def simulate_returns_against_dataframe(self, dataframe : pandas.DataFrame, ticker : str):
        """
        Returns a dict object replicative of Portfolio.Cash vars

        :param dataframe: The dataframe that will be iterated through
        :param ticker: The Ticker of the company to simulate returns
        :returns: A dict object 
        """
        ticker_performance = {
            "shares": 0,
        }

        oldest_action_time = pandas.to_datetime(dataframe["Time"].iloc[0])
        ticker_data = yfinance.download(ticker, oldest_action_time)

        for index, row in dataframe.iterrows():
            print(row)

        return ticker_performance
