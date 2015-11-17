from abcbank.transaction import *
from datetime import datetime

class Account:
    #Abstract class shouldn't be created via constructor
    def __init__(self):
        raise NotImplementedError("Must create a specific account type")

    #deposit
    def deposit(self, amount):
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        else:
            self.pending.append(Transaction(amount))
            self.transactionTotal += amount

    #withdraw, but ensure that account has enough money
    def withdraw(self, amount):
        self.updateBalance()
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        elif (self.balance < amount):
            raise ValueError("amount must not exceed current account balance")
        else:
            self.pending.append(Transaction(-amount))
            self.transactionTotal -= amount

    #calculate interest at current balance for given number of days.
    #since account types are different this gets implemented separately for each account type
    def calculateInterest(self, numdays):
        raise NotImplementedError("Interest rate not implemented")        

    #Update balance while calculating interest according to transaction dates
    def updateBalance(self):
        if len(self.pending) == 0:
            return self.balance
        else:
            days = 0
            transaction = self.pending.pop(0)
            if len(self.history) != 0:
                days = (transaction.transactionDate - self.history[len(self.history) - 1].transactionDate).days
            self.history.append(transaction)
            self.balance += (self.calculateInterest(days, transaction.transactionDate) + transaction.amount)
            return self.updateBalance()

    #Total amount of interest earned (unnecessary, but is here due to confusion of what this function was meant to originally do)
    def interestEarned(self):
        self.updateBalance()
        return self.balance - self.transactionTotal

    #Account type to string, implemented in sub-classes
    def accountString(self):
        raise NotImplementedError("Account type string not implemented")

    #Yearly interest, this is what "interestEarned" used to be
    def yearlyInterest(self):
        self.updateBalance()
        return self.calculateInterest(365, datetime.now())

    #Format account statement
    def accountStatement(self):
        self.updateBalance()
        header = self.accountString()
        transactions = "\nNone\n"
        total = "Total " + toDollars(self.balance) + "\n"

        if (len(self.history) != 0):
            i = len(self.history) - 1
            transactions = "\n"
            while i >= 0:
                transactions += "  " + self.history[i].getType() + " " + toDollars(abs(self.history[i].amount)) + "\n"
                i -= 1

        return header + transactions + total

class CheckingAcc(Account):
    def __init__(self):
        self.balance = 0
        self.transactionTotal = 0
        self.history = []
        self.pending = []

    def calculateInterest(self, numdays, date):
        yearPart = numdays/365
        return round(self.balance * (pow(1.001, yearPart) - 1), 4)

    def accountString(self):
        return "\n\nChecking Account\n"

class SavingsAcc(Account):
    def __init__(self):
        self.balance = 0
        self.transactionTotal = 0
        self.history = []
        self.pending = []

    def calculateInterest(self, numdays, date):
        yearPart = numdays/365
        return round(min(1000,self.balance) * (pow(1.001, yearPart) - 1) + max(self.balance - 1000, 0) * (pow(1.002, yearPart) - 1), 4)

    def accountString(self):
        return "\n\nSavings Account\n"

class MaxiSavingsAcc(Account):
    def __init__(self):
        self.balance = 0
        self.transactionTotal = 0
        self.lastWithdrawal = None
        self.history = []
        self.pending = []

    def withdraw(self, amount):
        self.updateBalance()
        if (amount <= 0):
            raise ValueError("amount must be greater than zero")
        elif (self.balance < amount):
            raise ValueError("amount must not exceed current account balance")
        else:
            transaction = Transaction(-amount)
            self.pending.append(transaction)
            self.lastWithdrawal = transaction.transactionDate
            self.transactionTotal -= amount

    def calculateInterest(self, numdays, date):
        if self.lastWithdrawal == None:
            yearPart = numdays/365
            return round(self.balance * (pow(1.05, yearPart) - 1), 4)
        
        sinceWithdrawal = (date - self.lastWithdrawal).days 

        if ((sinceWithdrawal - numdays) > 10):
            yearPart = numdays/365
            return round(self.balance * (pow(1.05, yearPart) - 1), 4)
        else:
            yearPart1 = min(numdays, (numdays + 10 - sinceWithdrawal))/365
            yearPart2 = numdays/365 - yearPart1
            return round(self.balance * (pow(1.001, yearPart1) - 1) + self.balance * (pow(1.05, yearPart2) - 1), 4)

    def accountString(self):
        return "\n\nMaxi Savings Account\n"

