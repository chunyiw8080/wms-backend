import os
import sys
from decimal import Decimal
from typing import Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from baseDB import DatabaseManager


class OrdersDB(DatabaseManager):
    def list_orders(self, order_id: str = None) -> Dict[str, str]:
        query = """
        SELECT * FROM orders
        """
        if order_id:
            query += " WHERE orders.order_id = %s"
            params = (order_id,)
            return self.fetch_query(query, params, single=True)
        else:
            return self.fetch_query(query, single=False)

    def search_orders_by_condition(self, conditions: Dict[str, str]) -> Dict[str, str]:
        params = []
        query = """
        SELECT * FROM orders
        """
        non_empty_conditions = []
        params = []
        for key, value in conditions.items():
            if value:
                non_empty_conditions.append(f"{key} = %s")
                params.append(value)

        if conditions:
            query += " WHERE " + " AND ".join(non_empty_conditions)

        return self.fetch_query(query, params, single=False)

    def create_order(self, data: Dict) -> bool:
        query = """
        INSERT INTO orders (order_id, order_type, cargo_id, price, provider, project, status, employee_id, published_at, processed_at, count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data['order_id'], data['order_type'], data['cargo_id'], data['price'], data['provider'], data['project'],
            data['status'], data['employee_id'], data['published_at'], data['processed_at'], data['count']
        )
        res = self.execute_query(query, params)
        return res

    def get_today_order_count(self):
        query = """
        SELECT COUNT(*) as count FROM orders
        WHERE DATE(published_at) = CURDATE()
        """
        result = self.fetch_query(query, single=True)
        return result['count']

    def get_cargo_id_by_cargo_name_model(self, cargo_name: str, model: str) -> Dict[str, str]:
        query = """
        SELECT orders.cargo_id FROM orders
        JOIN inventory ON orders.cargo_id = inventory.cargo_id
        WHERE inventory.cargo_name = %s AND inventory.model = %s;
        """
        params = (cargo_name, model, )
        return self.fetch_query(query, params, single=True)

    def update_order_by_id(self, order_id: str, status: str = None, data: Dict = None) -> bool:
        params = []
        if status:
            query = """
            UPDATE orders SET status = %s, processed_at = CURRENT_TIMESTAMP
            WHERE order_id = %s
            """
            params = (status, order_id)
        else:
            query = """
            UPDATE orders SET price = %s, provider = %s, project = %s, status = %s, employee_id = %s, processed_at = CURDATE()
            WHERE order_id = %s
            """
            params = (data['price'], data['provider'], data['project'], data['status'], data['employee_id'], order_id)
        res = self.execute_query(query, params)
        return res

    def order_exists(self, order_id: str) -> bool:
        query = """
        SELECT COUNT(*) as count FROM orders
        WHERE order_id = %s
        """
        params = (order_id,)
        result = self.fetch_query(query, params, single=True)
        return result['count'] > 0

    def update_inventory(self, order_id: str, amount: int, price: Decimal = None) -> bool:
        query = """
        UPDATE inventory
        SET count = %s
        """
        if price:
            query += ", price = %s WHERE cargo_id = (SELECT cargo_id FROM orders WHERE order_id = %s);"
            params = (amount, price, order_id)
        else:
            query += "WHERE cargo_id = (SELECT cargo_id FROM orders WHERE order_id = %s);"
            params = (amount, order_id)
        res = self.execute_query(query, params)
        return res

    def get_employee_id_by_name(self, employee_name: str):
        query = """
        SELECT employee_id FROM employee
        WHERE employee_name = %s
        """
        params = (employee_name,)
        return self.fetch_query(query, params, single=True)
