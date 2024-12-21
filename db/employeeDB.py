import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from baseDB import DatabaseManager


class EmployeeDB(DatabaseManager):
    def fetch_employees(self):
        query = """
        SELECT * FROM employee
        WHERE deleted = 0;
        """
        return self.fetch_query(query)

    def employee_exists(self, employee_id: str = None, employee_name: str = None) -> bool:
        params = []
        query = """
        SELECT COUNT(*) as count FROM employee
        """
        if employee_id:
            query += " WHERE employee_id = %s"
            params.append(employee_id)
        if employee_name:
            print(123)
            query += " WHERE employee_name = %s"
            params.append(employee_name)

        result = self.fetch_query(query, params, single=True)
        print(result)
        return result['count'] > 0

    def create_employee(self, data: dict) -> bool:
        query = """
        INSERT INTO employee (employee_id, employee_name, gender, position)
        VALUES (%s, %s, %s, %s)
        """
        params = (data['employee_id'], data['employee_name'], data['gender'], data['position'])
        result = self.execute_query(query, params)
        return result

    def get_employee_by_name_or_id(self, employee_id: str = None, employee_name: str = None):
        query = """
        SELECT * FROM employee
        """
        params = []
        if employee_id:
            query += " WHERE employee_id = %s"
            params.append(employee_id)
        if employee_name:
            query += " WHERE employee_name = %s"
            params.append(employee_name)
        return self.fetch_query(query, params, single=True)

    def search_employee(self, condition: str):
        query = """
        SELECT * FROM employee
        WHERE employee_name LIKE %s OR position LIKE %s;
        """
        condition = f"%{condition}%"
        params = (condition, condition, )
        return self.fetch_query(query, params, single=False)

    def get_employee_id_by_name(self, employee_name: str = None):
        query = """
        SELECT employee_id FROM employee
        WHERE employee_name = %s
        """
        params = (employee_name, )
        return self.fetch_query(query, params, single=True)

    def delete_employee(self, employee_id: str) -> bool:
        query = """
        UPDATE employee
        SET deleted = 1
        WHERE employee_id = %s
        """
        params = (employee_id,)
        result = self.execute_query(query, params)
        return result

    def update_employee(self, employee_id:str, data: dict) -> bool:
        query = """
        UPDATE employee SET employee_name = %s, gender = %s, position = %s 
        WHERE employee_id = %s
        """
        params = (data['employee_name'], data['gender'], data['position'], employee_id)
        print(params)
        return self.execute_query(query, params)

    def get_employee_count(self):
        query = """
        SELECT COUNT(*) as count FROM employee
        """
        count = self.fetch_query(query, single=True)
        return count['count']