import os
import sys
from decimal import Decimal
from typing import Dict
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from baseDB import DatabaseManager


class OrdersDB(DatabaseManager):
    def list_orders(self, order_id: str = None) -> Dict[str, str]:
        query = """
        SELECT *, price * count as total_price FROM orders
        """
        if order_id:
            query += " WHERE orders.order_id = %s"
            params = (order_id,)
            return self.fetch_query(query, params, single=True)
        else:
            return self.fetch_query(query, single=False)

    def get_full_orders(self):
        query = """
        SELECT 
            o.order_id, 
            o.order_type, 
            o.cargo_id, 
            i.cargo_name, 
            i.model, 
            i.categories, 
            o.price, 
            o.provider, 
            o.project, 
            o.status, 
            e.employee_name, 
            o.published_at, 
            o.processed_at, 
            o.count,
            i.specification,
            o.price * o.count as total_price
        FROM 
            orders o
        JOIN 
            inventory i ON o.cargo_id = i.cargo_id
        JOIN 
            employee e ON o.employee_id = e.employee_id
        ORDER BY o.order_id DESC 
        """
        return self.fetch_query(query)

    def get_orders_by_page(self, page=1, per_page=20):
        query = """
         SELECT 
            o.order_id, 
            o.order_type, 
            o.cargo_id, 
            i.cargo_name, 
            i.model, 
            i.categories, 
            o.price, 
            o.provider, 
            o.project, 
            o.status, 
            e.employee_name, 
            o.published_at, 
            o.processed_at, 
            o.count,
            i.specification,
            o.price * o.count as total_price
        FROM 
            orders o
        JOIN 
            inventory i ON o.cargo_id = i.cargo_id
        JOIN 
            employee e ON o.employee_id = e.employee_id
        ORDER BY o.order_id DESC 
        LIMIT %s OFFSET %s;
        """

        # WHERE  DATE_FORMAT(o.published_at, '%%Y-%%m') = DATE_FORMAT(CURRENT_DATE, '%%Y-%%m')
        # OFFSET 计算：从第 (page - 1) * per_page 条数据开始
        page = int(page)
        per_page = int(per_page)
        offset = (page - 1) * per_page
        params = (per_page, offset)  # 修正参数顺序
        print(per_page, offset)
        return self.fetch_query(query, params, single=False)

    def search_orders_by_condition(self, conditions: Dict[str, str] = None, order_id = None) -> Dict[str, str] or None:
        params = []
        query = """
            SELECT 
               o.order_id, 
               o.order_type, 
               o.cargo_id, 
               i.cargo_name, 
               i.model, 
               i.categories, 
               o.price, 
               o.provider, 
               o.project, 
               o.status, 
               e.employee_name, 
               o.published_at, 
               o.processed_at, 
               o.count,
               i.specification,
               o.price * o.count as total_price
           FROM 
               orders o
           JOIN 
               inventory i ON o.cargo_id = i.cargo_id
           JOIN 
               employee e ON o.employee_id = e.employee_id 
       """
        where_clauses = []
        if order_id:
            query += " WHERE o.order_id = %s"
            params.append(order_id,)
            return self.fetch_query(query, params, single=True)
        elif conditions:
            for key, value in conditions.items():
                if value:
                    where_clauses.append(f"{key} = %s")
                    params.append(value)
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
                print(query)
                return self.fetch_query(query, params, single=False)
        else:
            return None

    def create_order(self, data: Dict, single: bool = False) -> bool:
        exists = self.order_exists(data['order_id'])
        if exists:
            return False
        else:
            query = """
            INSERT INTO orders (order_id, order_type, cargo_id, price, provider, project, status, employee_id, published_at, processed_at, count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            if single is False:
                query_res = self.get_employee_id_by_name(data['employee_name'])
                employee_id = query_res.get('employee_id')
            else:
                employee_id = data['employee_id']
            params = (
                data['order_id'], data['order_type'], data['cargo_id'], data['price'], data['provider'], data['project'],
                data['status'], employee_id, data['published_at'], data['processed_at'], data['count']
            )
            print(params)
            res = self.execute_query(query, params)
            return res

    def get_today_order_count(self):
        query = """
        SELECT COUNT(*) as count FROM orders
        WHERE DATE(published_at) = CURDATE()
        """
        result = self.fetch_query(query, single=True)
        return result['count']

    def get_order_count(self):
        query = """
        SELECT COUNT(*) as count 
        FROM orders;
        """

        result = self.fetch_query(query, single=True)
        return result['count']

    def get_cargo_id_by_cargo_name_model(self, cargo_name: str, model: str) -> Dict[str, str]:
        query = """
        SELECT inventory.cargo_id FROM inventory
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
        print(result)
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

    def print_orders(self, order_id: str) -> Dict[str, str] or None:
        query = """
            SELECT 
               o.order_id, 
               o.order_type, 
               o.cargo_id, 
               i.cargo_name, 
               i.model, 
               i.categories, 
               o.price, 
               o.provider, 
               o.project, 
               o.status, 
               e.employee_name, 
               o.published_at, 
               o.processed_at, 
               o.count,
               i.specification,
               o.price * o.count as total_price
           FROM 
               orders o
           JOIN 
               inventory i ON o.cargo_id = i.cargo_id
           JOIN 
               employee e ON o.employee_id = e.employee_id 
            WHERE o.order_id = %s
       """
        params = (order_id,)
        res = self.fetch_query(query, params, single=True)
        return res

