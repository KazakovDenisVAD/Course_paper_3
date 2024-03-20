from utils.operations_func import load_operations_data
from utils.operations_func import sorted_and_executed_operations
from utils.operations_func import mask_card_number
from utils.operations_func import mask_account_number
import json


def test_mask_card_number():
    assert mask_card_number('Счет 123456789012345678901') == 'Счет **8901'
    assert mask_card_number('') == 'No card number provided'
    assert mask_card_number('Visa Classic 1234567890123456') == 'Visa Classic 1234 56** **** 3456'


def test_mask_account_number():
    assert mask_account_number('Счет 123456789012345678901') == 'Счет **8901'


def test_load_operations_data():
    with open('test_operations.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    assert type(data) is list
    assert len(data) > 0



def test_sorted_and_executed_operations():
    operations = [{'state': 'EXECUTED', 'date': '2023-01-02T12:00:00.000'}, {'state': 'PENDING', 'date': '2023-01-01T12:00:00.000'}, {'state': 'EXECUTED', 'date': '2023-01-01T12:00:00.000'}]
    assert len(sorted_and_executed_operations(operations)) == 2, "Должно возвращать только выполненные операции"
    assert sorted_and_executed_operations(operations)[0]['date'] > sorted_and_executed_operations(operations)[1]['date'], "Должно сортировать операции в обратном порядке"

