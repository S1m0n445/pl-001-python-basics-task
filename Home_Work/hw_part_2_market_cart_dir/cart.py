from typing import Final, cast
from crud import read_product
from storage import Product, PRODUCT_ID_INDEX, NAME_INDEX, PRICE_INDEX, QUANTITY_INDEX

CartLine = tuple[int, int]
LINE_PRODUCT_ID_INDEX: Final[int] = 0
LINE_QUANTITY_INDEX: Final[int] = 1


def find_cart_line(cart: list[CartLine], product_id: int) -> CartLine | None:
    for line in cart:
        if line[LINE_PRODUCT_ID_INDEX] == product_id:
            return line
    return None

def change_cart_quantity(cart: list[CartLine], product_id: int, delta: int) -> CartLine | None:
    for i, line in enumerate(cart):
        if line[LINE_PRODUCT_ID_INDEX] == product_id:
            new_qty = cast(int, line[LINE_QUANTITY_INDEX]) + delta
            if new_qty < 0:
                raise ValueError("cart quantity cannot be negative")
            if new_qty == 0:
                del cart[i]
                return (product_id, 0)
            cart[i] = (product_id, new_qty)
            return cart[i]
    if delta > 0:
        new_line = (product_id, delta)
        cart.append(new_line)
        return new_line
    return None

def _set_stock_quantity(storage: list[Product], product_id: int, new_quantity: int) -> None:
    for i, product in enumerate(storage):
        if product[PRODUCT_ID_INDEX] == product_id:
            pid, name, price, _ = product
            storage[i] = (pid, name, price, new_quantity)
            return
    raise ValueError("product with id " + str(product_id) + " not found in storage")

def add_to_cart(storage: list[Product], cart: list[CartLine], product_id: int, quantity: int) -> CartLine | None:
    product = read_product(storage, product_id)
    if product is None:
        return None
    stock_qty = cast(int, product[QUANTITY_INDEX])
    if stock_qty < quantity:
        print("not enough stock for product ", product_id, ": ", stock_qty, " available, ", quantity, " requested")
        return None
    _set_stock_quantity(storage, product_id, stock_qty - quantity)
    return change_cart_quantity(cart, product_id, quantity)

def remove_from_cart(storage: list[Product], cart: list[CartLine], product_id: int, quantity: int) -> CartLine | None:
    line = find_cart_line(cart, product_id)
    if line is None:
        print("product ", product_id, " is not in the cart")
        return None
    cart_qty = cast(int, line[LINE_QUANTITY_INDEX])
    if cart_qty < quantity:
        print("cart holds only ", cart_qty, " unit(s) of product ", product_id, ", cannot remove ", quantity)
        return None
    product = read_product(storage, product_id)
    if product is None:
        return None
    stock_qty = cast(int, product[QUANTITY_INDEX])
    _set_stock_quantity(storage, product_id, stock_qty + quantity)
    return change_cart_quantity(cart, product_id, -quantity)
