from decimal import Decimal
from typing import cast # без cast выдавал ошибку, по-другому не смог исправить
from storage import Product, PRODUCT_ID_INDEX, NAME_INDEX, PRICE_INDEX, QUANTITY_INDEX, PRODUCT_ID_MIN
from utils import normalize_price


def generate_product_id(storage: list[Product]) -> int:
    if not storage:
        return PRODUCT_ID_MIN
    return max(cast(int, product[PRODUCT_ID_INDEX]) for product in storage) + 1

def create_product(storage: list[Product], fields: tuple[str, Decimal, int]) -> int | None:
    name, price, quantity = fields
    for product in storage:
        if product[NAME_INDEX] == name:
            print("product name '", name, "' is already taken")
            return None
    product_id = generate_product_id(storage)
    normalized_price = normalize_price(price)
    storage.append((product_id, name, normalized_price, quantity))
    return product_id

def read_product(storage: list[Product], product_id: int) -> Product | None:
    for product in storage:
        if product[PRODUCT_ID_INDEX] == product_id:
            return product
    print("no product with id ", product_id)
    return None

def update_product(storage: list[Product], product_id: int, fields: tuple[str, Decimal, int]) -> Product | None:
    name, price, quantity = fields
    for i, product in enumerate(storage):
        if product[PRODUCT_ID_INDEX] == product_id:
            normalized_price = normalize_price(price)
            updated = (product_id, name, normalized_price, quantity)
            storage[i] = updated
            return updated
    print("no product with id ", product_id)
    return None

def delete_product(storage: list[Product], product_id: int) -> int | None:
    for i, product in enumerate(storage):
        if product[PRODUCT_ID_INDEX] == product_id:
            del storage[i]
            return product_id
    print("no product with id ", product_id)
    return None

