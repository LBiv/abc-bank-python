from nose.tools import assert_is_instance, assert_equals
import sys

sys.path.append('../abcbank')

from abcbank.transaction import Transaction


def test_type():
    t = Transaction(5)
    assert_is_instance(t, Transaction, "correct type")

def test_type_string():
    deposit = Transaction(5)
    withdrawal = Transaction(-5)
    assert_equals("deposit", deposit.getType())
    assert_equals("withdrawal", withdrawal.getType())


