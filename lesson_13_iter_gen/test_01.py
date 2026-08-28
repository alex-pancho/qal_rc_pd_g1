import pytest
from calc import add


@pytest.mark.parametrize(
        "value_1,value_2,expected_result",
        [
            (2, 3, 5),
            (2, 2, 4),
            (1, 1, 2),
            #(2, 6, 2)
        ],
        ids=[
            "test a",
            "Tes BBB",
            "Test in my honored name Im best"
        ]
)
def test_add(value_1, value_2, expected_result):
    # Acc
    # value_1 = 2
    # value_2 = 3
    # expected_result = 5
    # Act
    result_action = add(value_1, value_2)
    # Assert
    assert result_action == expected_result, f"Waiting for {expected_result}, but get {result_action}"
