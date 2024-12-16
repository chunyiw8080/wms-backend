import os
import sys
from typing import Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from baseDB import DatabaseManager


class HistoryDB(DatabaseManager):
    def get_history_by_date(self, year, month):
        query = """
        SELECT * FROM history
        WHERE year = %s and month = %s
        """
        params = (year, month)
        return self.fetch_query(query, params, single=False)

    def create_record(self, data: Dict[str, str]) -> bool:
        query = """
        INSERT INTO history(id, year, month, cargo_name, model, categories, starting_price, starting_count, starting_total_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (data['record_id'], data['year'], data['month'], data['cargo_name'], data['model'], data['categories'],
                  data['starting_price'], data['starting_count'], data['starting_total_price'])
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

    def import_record(self, data: list[dict]) -> tuple[bool, int, int]:
        failed = 0
        succeed = 0
        query = """
        INSERT INTO history(id, year, month, cargo_name, model, categories, starting_price, starting_count, starting_total_price, closing_price, closing_count, closing_total_price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for record in data:
            params = tuple(record.values())
            record_id = self.get_record_id(params)
            print(f'record_id: {record_id}')
            params_list = list(params)
            params_list.insert(0, record_id)
            new_params = tuple(params_list)
            print(f'params: {new_params}')
            res = self.execute_query(query, new_params)
            if not res:
                failed += 1
            else:
                succeed += 1

        return succeed != 0, succeed, failed

    def get_record_id(self, data: tuple):
        cargo_name = data[2]
        model = data[3]
        query = """
        SELECT cargo_id FROM inventory
        WHERE cargo_name = %s and model = %s
        """
        result = self.fetch_query(query, (cargo_name, model), single=True)
        cargo_id = result.get('cargo_id')
        if not cargo_id:
            return None
        else:
            year = data[0]
            month = data[1]
            if 1 <= int(month) <= 9:
                month = f'0{month}'
            record_id = f'{year}{month}{cargo_id}'
            return record_id

