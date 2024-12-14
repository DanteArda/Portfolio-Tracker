class Portfolio:
    """General Interface for an Investment Portfolio."""

    # Attributes
    @staticmethod
    def filter_attributes(cls : object) -> dict:
        """
        Filters through __dict__, removing any key value that begins with '_'; therefore removing internal attributes.

        Args:
            cls (object): A general object.
            
        Returns:
            dict: The filtered attributes.
        """
        return {key : value for key, value in cls.__dict__.items() if not key.startswith('_')}
    
    # Attributes - Setting
    @staticmethod
    def write_to(cls : object, data : dict):
        """
        Overwrites the attributes in a class.

        The data to overwrite can be retrieved by using a filter method, e.g. filter_new_cash_attributes to retrieve a template for the Cash attributes.

        Args:
            cls (object): The attributes of the class to be overwritten.
            data (dict): The data to be flushed onto the attributes.
        """
        for key, value in data.items():
            if hasattr(cls, key):
                setattr(cls, key, value)

    class Cash:
        """
        Interface for portfolio balances.

        Attributes:
            blocked (int): Cash currently in process for a transaction.
            free (int): Idle liquid cash.
            invested (int): Total value of instruments net profit and loss.
            profit_and_loss (int): Current profit and loss on all open positions.
            realized (int): Total realized profit or loss.
            total (int): Total cash held after price movements.
            total_dividend (int): Total interest from dividend payments.
        """
        blocked = 0
        free = 0
        invested = 0
        profit_and_loss = 0
        realized = 0
        total = 0
        total_dividend = 0
