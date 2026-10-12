from typing import Final
from decimal import Decimal, ROUND_HALF_UP
from storage import Product

PRICE_PRECISION: Final[int] = 2
PRICE_STEP: Final[Decimal] = Decimal(1).scaleb(-PRICE_PRECISION)
TABLE_HEADERS: Final[tuple[str, ...]] = ("ID", "name", "price", "quantity") #изначально было TABLE_HEADERS: Final = ("ID", "name", "price", "quantity"), вс код жаловался на типы, поэтому исправил, чтоб красным не горел 


def normalize_price(price: Decimal) -> Decimal:
    return price.quantize(PRICE_STEP, rounding=ROUND_HALF_UP)

def normalize_product_name(name: str) -> str:
    name = name.strip()
    name = name.lower()
    words = name.split()
    result = " ".join(words)
    return result

def get_storage_str_representation(storage: list[Product]) -> str:
    rows: list[tuple[str, ...]] = [tuple(TABLE_HEADERS)] #тут так же анотировал, чтобы вс код не ругался
    for product in storage:
        product_id, name, price, quantity = product
        row = (str(product_id), name, str(price), str(quantity))
        rows.append(row)
    widths = []
    for column in range(4):
        max_width = 0
        for row in rows:
            if len(row[column]) > max_width:
                max_width = len(row[column])
        widths.append(max_width)

    lines = []
    for row in rows:
        cells = []
        for column in range(4):
            value = row[column]
            spaces = widths[column] - len(value)
            cell = " " + value + " " * spaces + " "
            cells.append(cell)
        line = "|" + "|".join(cells) + "|"
        lines.append(line)
    separator_cells = []
    for width in widths:
        separator_cells.append("-" * (width + 2))
    separator = "|" + "|".join(separator_cells) + "|"

    result_lines = [lines[0], separator]
    for i in range(1, len(lines)):
        result_lines.append(lines[i])

    return "\n".join(result_lines)

