import os
import sys
from typing import Dict, List
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from baseDB import DatabaseManager


class InventoryDB(DatabaseManager):
    def show_inventories(self):
        query = """
        SELECT * FROM inventory
        """
        return self.fetch_query(query)

    def show_inventory_count(self, data: dict = None) -> int:
        """此函数计算库存条目总数，不包括已经被标记为删除的条目"""
        params = []
        query = """
        SELECT COUNT(*) as count FROM inventory
        WHERE deleted IS FALSE
        """
        if data:
            if data["category"]:
                query += f" AND categories = %s"
                params.append(data["category"])
            if data["cargo_name"]:
                query += f" AND cargo_name = %s"
                params.append(data["cargo_name"])
            if data["model"]:
                query += f" AND model = %s"
                params.append(data["model"])

            result = self.fetch_query(query, params, single=True)
        else:
            result = self.fetch_query(query, single=True)
        print(result)
        return result['count']

    def show_inventories_paginated(self, page=1, per_page=20, category: str = None):
        """此函数根据页数返回库存数据，每页默认20条"""
        offset = (page - 1) * per_page
        if category:
            query = """
            SELECT cargo_id, cargo_name, model, categories, count, price, specification, deleted, count * price as total_price FROM inventory
            WHERE deleted IS FALSE AND categories = %s
            LIMIT %s OFFSET %s
            """
            params = (category, per_page, offset)
        else:
            query = """
            SELECT cargo_id, cargo_name, model, categories, count, price, specification, deleted, count * price as total_price FROM inventory
            WHERE deleted IS FALSE
            LIMIT %s OFFSET %s
            """
            params = (per_page, offset)
        return self.fetch_query(query, params, single=False)

    def get_all_inventories(self, category: str = None) -> List[Dict]:
        if category:
            query = """
            SELECT cargo_id, cargo_name, model, categories, count, price, specification, deleted, count * price as total_price FROM inventory
            WHERE deleted IS FALSE AND categories = %s
            """
            params = (category, )
        else:
            query = """
            SELECT cargo_id, cargo_name, model, categories, count, price, specification, deleted, count * price as total_price FROM inventory
            WHERE deleted IS FALSE
            """
            params = ()
        return self.fetch_query(query, params, single=False)

    def get_inventory_by_id(self, cargo_id):
        """基于id获取库存条目信息"""
        query = """
        SELECT cargo_id, cargo_name, model, categories, count, price, specification, count * price as total_price FROM inventory
        WHERE cargo_id = %s
        """
        params = (cargo_id,)
        return self.fetch_query(query, params, single=True)

    def get_inventory_by_name_and_model(self, data: dict) -> bool:
        """基于货品名称和型号获取库存条目信息"""
        params = []
        conditions = []
        base_query = """
        SELECT cargo_id, cargo_name, model, categories, count, price, specification, count * price as total_price FROM inventory
        """
        # 动态生成查询条件
        if data.get('cargo_name'):
            conditions.append("cargo_name = %s")
            params.append(data['cargo_name'])
        if data.get('model'):
            conditions.append("model = %s")
            params.append(data['model'])
        # 拼接条件
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        query = base_query + ";"
        return self.fetch_query(query, params, single=False)

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
        """创建库存条目数据 - deleted字段在数据库中设置的默认值为False(0)，因此没有在这里设置"""
        query = """
        INSERT INTO inventory (cargo_id, cargo_name, model, categories, count, price, specification)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            inventory_info['cargo_id'], inventory_info['cargo_name'], inventory_info['model'],
            inventory_info['categories'], inventory_info['count'],
            inventory_info['price'], inventory_info['specification'])
        result = self.execute_query(query, params)
        return result

    def update_inventory(self, data: Dict[str, str]) -> bool:
        query = """
        UPDATE inventory SET cargo_name = %s, model = %s, categories = %s, specification = %s
        WHERE cargo_id = %s
        """
        params = (data['cargo_name'], data['model'], data['categories'], data['specification'],data['cargo_id'])
        result = self.execute_query(query, params)
        return result

    def get_total_inventory_count(self) -> int:
        """这个函数计算库存条目总数，包括已经被标记为删除的条目"""
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
            SELECT cargo_id, cargo_name, model, categories, count, price, specification, total_price
            FROM inventory
            WHERE cargo_id IN ({placeholders})
        """
        # 执行查询并传递 cargo_ids 作为参数
        return self.execute_query(query, cargo_ids)

    def get_categories(self):
        """获取所有的分类"""
        query = """
        SELECT categories FROM inventory
        GROUP BY categories
        """
        return self.fetch_query(query, params=None, single=False)

    def batch_delete_inventories(self, id_list: List[str]) -> bool:
        """批量删除数据 - 数据被标记为删除，不在前端显示，默认在被删除30天后从数据库中自动删除"""
        placeholders = ', '.join(['%s'] * len(id_list))
        query = f"UPDATE inventory SET deleted = 1 WHERE cargo_id IN ({placeholders})"
        print(f'delete query: {query}')
        result = self.execute_query(query, id_list)
        return result

    def search_by_category(self, category: str) -> bool:
        query = """
        SELECT cargo_id, cargo_name, model, categories, count, price, specification, count * price as total_price FROM inventory
        WHERE categories = %s AND deleted IS FALSE
        """
        params = (category,)
        return self.fetch_query(query, params, single=False)