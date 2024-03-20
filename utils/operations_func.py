import json
from datetime import datetime


def load_operations_data(file_path):
    """Функция открытия файла в режиме чтения"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for operation in data:
        if 'from' in operation:
            operation['from'] = mask_card_number(operation['from'])
        if 'to' in operation:
            operation['to'] = mask_account_number(operation['to'])

    return data


def sorted_and_executed_operations(operations):
    """Функция сортирвки по парметрам state и date"""
    executed_operations = [op for op in operations if op.get('state') == "EXECUTED"]
    sorted_operations = sorted(executed_operations, key=lambda x: datetime.strptime(x['date'], "%Y-%m-%dT%H:%M:%S.%f"),
                               reverse=True)
    return sorted_operations[:5]
    

def format_operation(operation):
    masked_from = mask_card_number(operation.get('from', ''))
    masked_to = mask_account_number(operation.get('to', ''))
    description_operation = f"{operation.get('description', '')}"
    formatted_date = datetime.strptime(operation['date'], "%Y-%m-%dT%H:%M:%S.%f").strftime('%d.%m.%Y')
    formatted_amount = f"{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}"

    return (f"{datetime.strptime(operation['date'], "%Y-%m-%dT%H:%M:%S.%f").strftime('%d.%m.%Y')} {operation.get('description', '')}\n"
            f"{mask_card_number(operation.get('from', ''))} -> {mask_account_number(operation.get('to', ''))}\n"
            f"{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}")


def mask_card_number(card: str):
    """Маскировка цифр номера карты"""
    card = card.split(' ')
    card_number = card.pop()
    card_name = " ".join(card)
    if card_name.lower() == "счет":
        mask_card_account = "**" + card_number[-4:]
        return f"{card_name} {mask_card_account}"
    elif card_name.lower() == "":
        return "No card number provided"
    else:
        mask_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        return f"{card_name} {mask_card}"


def mask_account_number(account_number):
    """Маскировка номера счета"""
    parts = account_number.split(' ', 1)
    if len(parts) != 2:
        account_number = parts[1]
        return account_number
    if len(account_number) > 6:
        masked_account_number = '**' + account_number[-4:]
        masked = parts[0] + ' ' + masked_account_number
        return masked
    else:
        return "No account number provided"


def main():
    operations_data = load_operations_data('operations.json')
    executed_operations = sorted_and_executed_operations(operations_data)

    for operation in executed_operations:
        formatted_operations = format_operation(operation)
        print(formatted_operations)
        print()


if __name__ == '__main__':
    main()