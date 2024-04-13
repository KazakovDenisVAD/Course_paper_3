import json
from copy import deepcopy
from datetime import datetime


def load_operations_data(file_path):
    """Функция открытия файла в режиме чтения"""

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for operation in data:
        if 'from' in operation:
            operation['from'] = mask_credential(operation['from'])
        if 'to' in operation:
            operation['to'] = mask_credential(operation['to'])

    return data


def sorted_and_executed_operations(operations):
    """Функция сортирвки по парметрам state и date"""

    executed_operations = [op for op in operations if op.get('state') == "EXECUTED"]
    sorted_operations = sorted(
        executed_operations,
        key=lambda x: datetime.strptime(x['date'], "%Y-%m-%dT%H:%M:%S.%f"),
        reverse=True,
    )
    return sorted_operations[:5]


def format_operation(operation):
    masked_from = operation.get('from', 'No data available')
    masked_to = operation.get('to', 'No data available')
    description_operation = f"{operation.get('description', '')}"
    formatted_date = datetime.strptime(
        operation['date'],
        "%Y-%m-%dT%H:%M:%S.%f"
    ).strftime('%d.%m.%Y')
    formatted_amount = f"{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}"

    return (
        f"{formatted_date} {description_operation}\n"
        f"{masked_from} -> {masked_to}\n"
        f"{formatted_amount}"
    )


def mask_credential(credential: str) -> str:
    """Маскировка чувствительных данных о счете/карте"""

    CARD_SPLIT_SIZE = 4
    CARD_NUMBER_LEN = 16

    if not credential:
        return credential

    credential_name = " ".join([
        name for name in credential.split()
        if name.isalpha()
    ])

    # Получим только числа из карты/счета
    credential_numbers: str = "".join(
        [
            number for number in credential
            if number.isdigit()
        ]
    )

    if len(credential_numbers) == CARD_NUMBER_LEN:
        # Делим строку чисел карты на чанки строк -> ["1234", "5678", ...].
        credential_numbers: list[str] = [
           "".join(tpl) for tpl in list(zip(*[iter(credential_numbers)] * CARD_SPLIT_SIZE))
        ]
        return f"{credential_name} {mask_card_number(credential_numbers)}"

    elif len(credential_numbers) > CARD_NUMBER_LEN:
        return f"{credential_name} {mask_account_number(credential_numbers)}"

    raise ValueError(f"Непредвидимые данные карты/счета {credential_numbers}")


def mask_card_number(card: list[str]) -> str:
    """Маскировка цифр номера карты"""

    card_parts_copy = deepcopy(card)
    for i, card_part in enumerate(card, 1):
        match i:
            case 1 | 4:
                card_parts_copy[i - 1] = card_part
            case 2:
                card_parts_copy[i - 1] = f"{card_part[:2]}**"
            case 3:
                card_parts_copy[i - 1] = "****"

    return " ".join(card_parts_copy)


def mask_account_number(account_number: str) -> str:
    """Маскировка номера счета"""

    return f"**{account_number[-4:]}"
