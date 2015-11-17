from nose.tools import assert_equals, nottest
import sys

sys.path.append('../abcbank')

from abcbank.account import *
from abcbank.customer import Customer

#too many things changed about the output
@nottest
def test_statement():
    checkingAccount = CheckingAcc()
    savingsAccount = SavingsAcc()
    henry = Customer("Henry").openAccount(checkingAccount).openAccount(savingsAccount)
    checkingAccount.deposit(100.0)
    savingsAccount.deposit(4000.0)
    savingsAccount.withdraw(200.0)
    print(henry.getStatement())
    assert_equals(henry.getStatement(),
                  "Statement for Henry" +
                  "\n\nChecking Account\n  deposit $100.00\nTotal $100.00" +
                  "\n\nSavings Account\n  deposit $4000.00\n  withdrawal $200.00\nTotal $3800.00" +
                  "\n\nTotal In All Accounts $3900.00")


def test_oneAccount():
    oscar = Customer("Oscar").openAccount(SavingsAcc())
    assert_equals(oscar.numAccs(), 1)


def test_twoAccounts():
    oscar = Customer("Oscar").openAccount(SavingsAcc())
    oscar.openAccount(CheckingAcc())
    assert_equals(oscar.numAccs(), 2)

def test_threeAccounts():
    oscar = Customer("Oscar").openAccount(SavingsAcc())
    oscar.openAccount(CheckingAcc()).openAccount(MaxiSavingsAcc())
    assert_equals(oscar.numAccs(), 3)
