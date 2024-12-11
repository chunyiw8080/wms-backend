import os
import sys
from typing import Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from baseDB import DatabaseManager


class ProviderProjectDB(DatabaseManager):
    def list(self, table_name: str) -> Dict[str, str]:
        query = f"SELECT * FROM {table_name}"
        return self.fetch_query(query, params=None, single=False)

    def create(self, table_name: str, filed_name: str, value: str) -> bool:
        query = f"INSERT INTO {table_name} ({filed_name}) VALUES (%s)"
        params = (value, )
        return self.execute_query(query, params)

    def delete(self, table_name: str, filed_name: str, value: str) -> bool:
        query = f"DELETE FROM {table_name} WHERE {filed_name} = %s"
        params = (value, )
        return self.execute_query(query, params)

    def data_exists(self, table_name: str, filed_name: str, value: str) -> bool:
        query = f"SELECT COUNT(*) as count FROM {table_name} WHERE {filed_name} = %s"
        params = (value, )
        res = self.fetch_query(query, params, single=True)
        return res['count'] > 0

    def search(self, table_name: str, filed_name: str, value: str):
        query = f"SELECT * FROM {table_name} WHERE {filed_name} = %s"
        params = (value,)
        res = self.fetch_query(query, params, single=True)
        return res

    def update(self, table_name: str, filed_name: str, value: str, origin_value: str) -> bool:
        query = f"UPDATE {table_name} SET {filed_name} = %s WHERE {filed_name} = %s"
        params = (value, origin_value, )
        return self.execute_query(query, params)
