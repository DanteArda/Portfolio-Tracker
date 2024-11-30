class Portfolio:
    """General Interface for an Investment Portfolio."""

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
        """
        blocked = 0
        free = 0
        invested = 0
        profit_and_loss = 0
        realized = 0
        total = 0

