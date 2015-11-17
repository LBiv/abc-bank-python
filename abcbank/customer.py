from abcbank.account import *
from abcbank.transaction import *


class Customer:
    def __init__(self, name):
        self.name = name
        self.accounts = []

    def openAccount(self, account):
        self.accounts.append(account)
        return self

    def numAccs(self):
        return len(self.accounts)

    def totalInterestEarned(self):
        return sum([a.interestEarned() for a in self.accounts])

    def depositTo(self, index_to, amount):
        if (index_to >= len(self.accounts)):
            raise ValueError("Invalid account index")
        self.accounts[index_to].deposit(amount)

    def withdrawFrom(self, index_from, amount):
        if (index_from >= len(self.accounts)):
            raise ValueError("Invalid account index")
        self.accounts[index_from].withdraw(amount)

    def customerYearlyInterest(self):
        return sum([a.yearlyInterest() for a in self.accounts])

    # This method gets a statement
    def getStatement(self):
        # JIRA-123 Change by Joe Bloggs 29/7/1988 start
        statement = None  # reset statement to null here
        # JIRA-123 Change by Joe Bloggs 29/7/1988 end
        totalAcrossAllAccounts = sum([a.updateBalance() for a in self.accounts])
        statement = "Statement for %s" % self.name
        for account in self.accounts:
            statement = statement + account.accountStatement()
        statement = statement + "\n\nTotal In All Accounts " + toDollars(totalAcrossAllAccounts)
        return statement

    def transfer(self, index_from, index_to, amount):
        if ((index_from >= len(self.accounts)) or (index_to >= len(self.accounts))):
            raise ValueError("Invalid account index")
        self.accounts[index_from].withdraw(amount)
        self.accounts[index_to].deposit(amount)
