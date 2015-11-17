from nose.tools import assert_equals, raises, assert_true
import sys

sys.path.append('../abcbank')

from abcbank.account import *

@raises(NotImplementedError)
def test_constructor():
    a = Account()

@raises(ValueError)
def test_deposit0():
    a = CheckingAcc()
    a.deposit(0)

@raises(ValueError)
def test_withdraw0():
    a = CheckingAcc()
    a.withdraw(0)

@raises(ValueError)
def test_withdraw_limit():
    a = CheckingAcc()
    a.withdraw(5)

def test_deposit():
    a = SavingsAcc()
    a.deposit(5)
    assert_equals(a.updateBalance(), 5)

def test_withdraw():
    a = SavingsAcc()
    a.deposit(5)
    a.withdraw(4)
    assert_equals(a.updateBalance(), 1)

def test_checking_interest():
    a = CheckingAcc()
    a.deposit(1000)
    a.updateBalance()
    interest = a.calculateInterest(365, None)
    assert_equals(interest, 1)

def test_checking_yearly_interest():
    a = CheckingAcc()
    a.deposit(1000)
    interest = a.yearlyInterest()
    assert_equals(interest, 1)

def test_savings_yearly_interest1():
    a = SavingsAcc()
    a.deposit(1000)
    interest = a.yearlyInterest()
    assert_equals(interest, 1)

def test_savings_yearly_interest2():
    a = SavingsAcc()
    a.deposit(2000)
    interest = a.yearlyInterest()
    assert_equals(interest, 3)

def test_maxi_yearly_interest1():
    a = MaxiSavingsAcc()
    a.deposit(1000)
    interest = a.yearlyInterest()
    assert_equals(interest, 50)

def test_maxi_yearly_interest2():
    a = MaxiSavingsAcc()
    a.deposit(1100)
    a.withdraw(100)
    interest = a.yearlyInterest()
    assert_true(interest < 50)
