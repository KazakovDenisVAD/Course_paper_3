import json

import pytest

from utils import (
    sorted_and_executed_operations,
    mask_credential,
    load_operations_data,
)


@pytest.fixture
def operations_data(tmp_path):
    file_path = tmp_path / "operations.json"
    CONTENT = [
        {
            "from": "90424923579946435907",
            "to": "Visa Platinum 1246377376343588",
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


def test_mask_credential():
    assert mask_credential('Счет 123456789012345678901') == 'Счет **8901'
    assert mask_credential('') == ''
    assert mask_credential('Visa Classic 1234567890123456') == 'Visa Classic 1234 56** **** 3456'

    with pytest.raises(ValueError):
        mask_credential('3428234')


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
