from decimal import Decimal,InvalidOperation
from typing import Final
from crud import create_product, delete_product, read_product, update_product
from storage import Product
from utils import get_storage_str_representation

PROMPT: Final[str] = "admin> "
HELP_TEXT: Final[str] = """Available commands:
  help                                       show this message
  exit                                       leave the console
  show                                       print the whole stor as a table
  create <name...> <price> <quantity>        add a product, print its new id
  read <id>                                  print the product with that id
  update <id> <name...> <price> <quantity>   overwrite that product's fields
  delete <id>                                remove the product with that id

For create and update the price and quantity are the last two words of the
line; everything before them is the product name, so it may contain spaces
(for example "Gibson SG Junior") and needs no quoting."""


def show_help() -> None:
    print(HELP_TEXT)

def print_result(result: object) -> None:
    if result is not None:
        print(result)

def run_command(storage: list[Product], line: str) -> bool:
    words = line.split()

    if len(words) == 1:
        command = words[0]
        if command == "help":
            show_help()
            return True
        if command == "exit":
            return False
        if command == "show":
            print(get_storage_str_representation(storage))
            return True

    if len(words) == 2 and words[0] == "read":
        product_id = int(words[1])
        result = read_product(storage, product_id)
        print_result(result)
        return True

    if len(words) == 2 and words[0] == "delete":
        product_id = int(words[1])
        result = delete_product(storage, product_id)
        print_result(result)
        return True

    if len(words) >= 4 and words[0] == "create":
        name_words = words[1:-2]
        name = " ".join(name_words)
        price = Decimal(words[-2])
        quantity = int(words[-1])
        result = create_product(storage, (name, price, quantity))
        print_result(result)
        return True

    if len(words) >= 5 and words[0] == "update":
        product_id = int(words[1])
        name_words = words[2:-2]
        name = " ".join(name_words)
        price = Decimal(words[-2])
        quantity = int(words[-1])
        result = update_product(storage, product_id, (name, price, quantity))
        print_result(result)
        return True

    print("'" + line + "' is not a command")
    return True

def main() -> None:
    storage: list[Product] = []
    keep_going = True
    while keep_going:
        line = input(PROMPT)
        line = line.strip()
        try:
            keep_going = run_command(storage, line)
        except (ValueError, InvalidOperation):
            print("'" + line + "' names a command but its arguments are invalid")


