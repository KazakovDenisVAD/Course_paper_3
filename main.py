from utils import load_operations_data, sorted_and_executed_operations, format_operation
from settings import JSON_DATA_PATH


def main():
    operations_data = load_operations_data(JSON_DATA_PATH)
    executed_operations = sorted_and_executed_operations(operations_data)

    for operation in executed_operations:
        formatted_operations = format_operation(operation)
        print(f"{formatted_operations}\n")


if __name__ == '__main__':
    main()
