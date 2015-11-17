from datetime import datetime


class Transaction:
    def __init__(self, amount):
        self.amount = amount
        self.transactionDate = datetime.now()

    def getType(self):
        if self.amount < 0:
            return "withdrawal"
        elif self.amount > 0:
            return "deposit"
        else:
            return "N\A"

def toDollars(number):
    return "${:1.2f}".format(number)
