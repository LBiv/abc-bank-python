from nose.tools import assert_equals, assert_true
import sys

sys.path.append('../abcbank')

from abcbank.account import *
from abcbank.bank import Bank
from abcbank.customer import Customer


def test_customer_summary():
    bank = Bank()
    john = Customer("John").openAccount(CheckingAcc())
    bank.addCustomer(john)
    assert_equals(bank.customerSummary(),
                  "Customer Summary\n - John (1 account)")


def test_checking_account():
    bank = Bank()
    checkingAccount = CheckingAcc()
    bill = Customer("Bill").openAccount(checkingAccount)
    bank.addCustomer(bill)
    checkingAccount.deposit(100.0)
    assert_equals(bank.totalYearlyInterest(), 0.1)


def test_savings_account():
    bank = Bank()
    savingsAccount = SavingsAcc()
    bank.addCustomer(Customer("Bill").openAccount(savingsAccount))
    savingsAccount.deposit(1500.0)
    assert_equals(bank.totalYearlyInterest(), 2.0)


def test_maxi_savings_account():
    bank = Bank()
    maxiAccount = MaxiSavingsAcc()
    bank.addCustomer(Customer("Bill").openAccount(maxiAccount))
    maxiAccount.deposit(3000.0)
    assert_equals(bank.totalYearlyInterest(), 150.0)

def test_maxi_savings_account():
    bank = Bank()
    maxiAccount = MaxiSavingsAcc()
    bank.addCustomer(Customer("Bill").openAccount(maxiAccount))
    maxiAccount.deposit(3100.0)
    maxiAccount.withdraw(100.0)
    assert_true(bank.totalYearlyInterest() < 150.0)
