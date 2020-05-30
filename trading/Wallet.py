"""
A wallet.
"""

class Wallet:
    # This is private because subclasses may need to be the only classes
    # that can access this property.
    _funds: float

    def __init__(self):
        self._funds = 0.0

    def getPortionOfFunds(self, portion: float) -> float:
        """
        Returns a ceretain portion of the funds.
        Precondition: 0 <= portion <= 1
        :param portion: the portion of the funds, e.g. 0.5 for 50%
        :return: the portion
        """
        return self._funds * portion

    def addFunds(self, amount: float):
        self._funds += amount

    def removeFunds(self, amount: float):
        self._funds -= amount

    def lacksFunds(self):
        return self._funds <= 0
