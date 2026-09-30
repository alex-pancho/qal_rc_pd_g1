from source import add, BankAccount
import logging
import pytest

logger = logging.getLogger()

def test_ab_positive():
    a = 1
    b = 2
    expected = 3
    # act
    actual_result = add(a,b)
    # assert
    logger.debug("Get data: %d, %d result %d, expected %d" % 
        (a, b, actual_result, expected))
    assert expected == actual_result, f"Get wrong data: {a}, {b} result {actual_result}, expected {expected}"

def test_add_plus():
    assert add(2, 3) == 5


def test_add_zero():
    assert add(10, 0) == 10


def test_add_minus():
    assert add(-1, -2) == -3

def test_ba_without_changes(zero_account):
    assert zero_account.balance == 0

def test_ba_fill_balance(zero_account):
    # act
    zero_account.deposit(0)
    # assert
    assert zero_account.balance == 0

@pytest.mark.parametrize("init_size,amount",
        [
            [0, 0.01],
            [100, 0.01],
            [0, 1],
            [100, 1],
            [0, 10.01],
            [100, 10.01],
            [0, 100000.01],
            [100, 10000.01],
        ],
        ids = [
            "zero",
            "100",
            "one",
            "101",
            "dsad",
            "sadsad",
            "ADD",
            "Test for SEPA according NBU leter 3.3",
        ])
def test_ba_fill_more_balance(init_size, amount):

    account = BankAccount(init_size)
    # act
    account.deposit(amount)
    # assert
    assert account.balance == amount + init_size

def test_ba_fill_negative(zero_account):
    # act
    with pytest.raises(ValueError) as e:
        zero_account.deposit(-1)
        # assert
    assert str(e.value) == "For deposit amount should be large than zero"

def test_1000_without_changes(one_000_account):
    assert one_000_account.balance == 1000
