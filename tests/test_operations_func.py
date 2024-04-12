import json

import pytest

from utils import (
    sorted_and_executed_operations,
    mask_account_number,
    mask_card_number,
    load_operations_data,
)


@pytest.fixture
def operations_data(tmp_path):
    file_path = tmp_path / "operations.json"
    CONTENT = [
        {
            "from": "1234567890123456",
            "to": "Счет 1234567890",
            "state": "EXECUTED",
            "date": "2023-01-01T12:00:00.000",
            "operationAmount": {
                "amount": 100,
                "currency": {
                    "name": "USD"
                }
            },
            "description": "Test Operation"
        }
    ]

    with open(file_path, "w") as f:
        json.dump(CONTENT, f)

    return file_path


def test_mask_card_number():
    assert mask_card_number('Счет 123456789012345678901') == 'Счет **8901'
    assert mask_card_number('') == 'No card number provided'
    assert mask_card_number('Visa Classic 1234567890123456') == 'Visa Classic 1234 56** **** 3456'


def test_mask_account_number():
    assert mask_account_number('Счет 123456789012345678901') == 'Счет **8901'


def test_load_operations_data(operations_data):
    result = load_operations_data(operations_data)
    assert type(result) is list
    assert len(result) > 0


def test_sorted_and_executed_operations():
    operations = [
        {'state': 'EXECUTED', 'date': '2023-01-02T12:00:00.000'},
        {'state': 'PENDING', 'date': '2023-01-01T12:00:00.000'},
        {'state': 'EXECUTED', 'date': '2023-01-01T12:00:00.000'},
    ]
    assert (
        len(sorted_and_executed_operations(operations)) == 2
    ), "Должно возвращать только выполненные операции"
    assert (
        sorted_and_executed_operations(operations)[0]['date']
        > sorted_and_executed_operations(operations)[1]['date']
    ), "Должно сортировать операции в обратном порядке"
