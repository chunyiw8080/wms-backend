import os
import sys
from typing import Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from baseDB import DatabaseManager


class HistoryDB(DatabaseManager):
    def get_all(self):
        query = """
        SELECT * FROM history
        """
        return self.fetch_query(query, params=None, single=False)

    def create_record(self, data: Dict[str, str]) -> bool:
        query = """
        INSERT INTO history(id, year, month, cargo_name, model, categories, starting_price, starting_count, starting_total_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (data['record_id'], data['year'], data['month'], data['cargo_name'], data['model'], data['categories'], data['starting_price'], data['starting_count'], data['starting_total_price'])
        res = self.execute_query(query, params)
        return res

    def get_history_id_by_date(self, year: str, month: str):
        query = """
        SELECT id FROM history 
        WHERE year=%s AND month=%s
        """
        params = (year, month)
        res = self.fetch_query(query, params, single=False)
        return res

    def update_record(self, id, data: Dict[str, str]) -> bool:
        query = """
        UPDATE history SET closing_count = %s, closing_price = %s, closing_total_price = %s
        WHERE id = %s
        """
        params = (data['closing_count'], data['closing_price'], data['closing_total_price'], id)
        res = self.execute_query(query, params)
        return res
