import os
import sys
from typing import Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from baseDB import DatabaseManager


class InventoryDB(DatabaseManager):
    def show_inventories(self):
        query = """
        SELECT cargo_id, cargo_name, model, categories, count, price, count * price as total_price FROM inventory
        """
        return self.fetch_query(query)

    def get_inventory_by_id(self, cargo_id):
        query = """
        SELECT cargo_id, cargo_name, model, categories, count, price, count * price as total_price FROM inventory
        WHERE cargo_id = %s
        """
        params = (cargo_id,)
        return self.fetch_query(query, params, single=True)

    def cargo_model_exists(self, cargo_name: str, model: str) -> bool:
        query = """
        SELECT COUNT(*) as count FROM inventory
        WHERE cargo_name = %s AND model = %s
        """
        params = (cargo_name, model)
        result = self.fetch_query(query, params, single=True)
        print(result['count'])
        return result['count'] > 0

    def create_inventory(self, inventory_info: Dict[str, str]) -> bool:
        query = """
        INSERT INTO inventory (cargo_id, cargo_name, model, categories, count, price)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            inventory_info['cargo_id'], inventory_info['cargo_name'], inventory_info['model'],
            inventory_info['categories'], inventory_info['count'],
            inventory_info['price'])
        result = self.execute_query(query, params)
        return result

    def update_inventory(self, data: Dict[str, str]) -> bool:
        query = """
        UPDATE inventory SET cargo_name = %s, model = %s, categories = %s
        WHERE cargo_id = %s
        """
        params = (data['cargo_name'], data['model'], data['categories'])
        result = self.execute_query(query, params)
        return result

    def get_total_inventory_count(self) -> int:
        query = """
        SELECT COUNT(*) as count FROM inventory
        """
        result = self.fetch_query(query, single=True)
        return result['count']

    def update_inventory_count(self, count:int, cargo_id: str) -> bool:
        query = """
        UPDATE inventory SET count = %s
        WHERE cargo_id = %s
        """
        params = (count, cargo_id)
        result = self.execute_query(query, params)
        return result

    def get_inventories_by_ids(self, cargo_ids):
        # 创建占位符数量等于 cargo_ids 数量的 SQL 查询
        placeholders = ', '.join(['%s'] * len(cargo_ids))
        query = f"""
            SELECT cargo_id, cargo_name, model, categories, count, price, total_price
            FROM inventory
            WHERE cargo_id IN ({placeholders})
        """
        # 执行查询并传递 cargo_ids 作为参数
        return self.execute_query(query, cargo_ids)
