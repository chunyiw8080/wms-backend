from decimal import Decimal

from db.ordersDB import OrdersDB
from db.inventoryDB import InventoryDB


def _get_cargo_id(db: OrdersDB, order_id: str) -> str:
    try:
        data = db.list_orders(order_id=order_id)
        cargo_id = data['cargo_id']
        return cargo_id
    except Exception as e:
        return None


def get_current_inventory_count(db: OrdersDB, order_id: str) -> int:
    cargo_id = _get_cargo_id(db, order_id)
    try:
        if cargo_id:
            with InventoryDB() as db:
                inventory_count = db.get_inventory_by_id(cargo_id)['count']
                return inventory_count
    except Exception as e:
        return None


def get_current_order_count(db: OrdersDB, order_id: str) -> int:
    try:
        data = db.list_orders(order_id=order_id)
        order_count = data['count']
        return order_count
    except Exception as e:
        return None


def get_current_price(db: OrdersDB, order_id: str) -> Decimal:
    cargo_id = _get_cargo_id(db, order_id)
    if cargo_id:
        try:
            with InventoryDB() as i_db:
                data = i_db.get_inventory_by_id(cargo_id)
                price = data['price']
                return price
        except Exception as e:
            return None
    else:
        return None


def get_order_price(db: OrdersDB, order_id: str) -> Decimal:
    try:
        data = db.list_orders(order_id=order_id)
        if data:
            price = data['price']
            return price
        else:
            return None
    except Exception as e:
        return None


def calculate_new_price(db: OrdersDB, order_id: str, order_type: str) -> Decimal:
    current_price = get_current_price(db, order_id)
    order_price = get_order_price(db, order_id)
    current_count = get_current_inventory_count(db, order_id)
    order_count = get_current_order_count(db, order_id)
    # print(f'current_price: {current_price}, order_price: {order_price}, current_count: {current_count}, order_count: {order_count}')

    if current_price and order_price and current_count and order_count:
        if order_type == 'inbound':
            new_price = (current_count * current_price + order_count * order_price) / (current_count + order_count)
            return new_price
        elif order_type == 'outbound':
            new_price = (current_price * current_count - order_count * order_price) / (current_count - order_count)
            return new_price
