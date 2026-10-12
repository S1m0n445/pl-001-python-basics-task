from decimal import Decimal
from typing import cast
from storage import Product, PRODUCT_ID_INDEX, NAME_INDEX, PRICE_INDEX, QUANTITY_INDEX, PRODUCT_ID_MIN
from utils import normalize_price, normalize_product_name


def generate_product_id(storage: list[Product]) -> int:
    if not storage:
        return PRODUCT_ID_MIN
    return max(cast(int, product[PRODUCT_ID_INDEX]) for product in storage) + 1

def create_product(storage: list[Product], fields: tuple[str, Decimal, int]) -> int | None:
    name, price, quantity = fields
    normalized_name = normalize_product_name(name)
    if normalized_name == "":
        print("product name must not be blank")
        return None

    for product in storage:
        if product[NAME_INDEX] == normalized_name:
            print("product name '" + normalized_name + "' is already taken")
            return None

    product_id = generate_product_id(storage)
    normalized_price = normalize_price(price)
    storage.append((product_id, normalized_name, normalized_price, quantity))
    return product_id

def read_product(storage: list[Product], product_id: int) -> Product | None:
    for product in storage:
        if product[PRODUCT_ID_INDEX] == product_id:
            return product
    print("no product with id " + str(product_id))
    return None

def update_product(storage: list[Product], product_id: int, fields: tuple[str, Decimal, int]) -> Product | None:
    name, price, quantity = fields
    normalized_name = normalize_product_name(name)

    if normalized_name == "":
        print("product name must not be blank")
        return None
    index = None
    for i, product in enumerate(storage):
        if product[PRODUCT_ID_INDEX] == product_id:
            index = i
            break

    if index is None:
        print("no product with id " + str(product_id))
        return None

    for product in storage:
        same_name = product[NAME_INDEX] == normalized_name
        other_id = product[PRODUCT_ID_INDEX] != product_id
        if same_name and other_id:
            print("product name '" + normalized_name + "' is already taken")
            return None

    normalized_price = normalize_price(price)
    updated = (product_id, normalized_name, normalized_price, quantity)
    storage[index] = updated
    return updated

def delete_product(storage: list[Product], product_id: int) -> int | None:
    for i, product in enumerate(storage):
        if product[PRODUCT_ID_INDEX] == product_id:
            del storage[i]
            return product_id
    print("no product with id " + str(product_id))
    return None
