import os
import sys
from typing import Dict

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from baseDB import DatabaseManager


class UserDB(DatabaseManager):
    def fetch_users(self) -> Dict[str, str]:
        """
        :return: Result of all users in the database
        """
        query = """
        SELECT * FROM user
        """
        return self.fetch_query(query)

    def fetch_user_by_id(self, user_id: str) -> Dict[str, str]:
        """
        :param user_id: User ID, primary key
        :return: Result of user by id
        """
        query = """
        SELECT * FROM user WHERE user_id = %s
        """
        params = (user_id,)
        return self.fetch_query(query, params, single=True)

    def login_authentications(self, username: str, password: str) -> Dict[str, str]:
        """
        :param username: Username received from front-end
        :param password: Password received from front-end
        :return: Query result
        """
        query = """
        SELECT * FROM user WHERE username = %s AND password = %s
        """
        params = (username, password)
        return self.fetch_query(query, params, single=True)

    def create_user(self, data: Dict[str, str]) -> bool:
        """
        :param data: User information used to create new user
        :return: Result of the execution (True or False)
        """
        query = """
        INSERT INTO user (user_id, username, password, employee_id, created_at, status, privilege)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            data["user_id"], data["username"], data["password"], data["employee_id"], data["created_at"],
            data["status"],
            data["privilege"])
        return self.execute_query(query, params)

    def delete_user(self, user_id: str) -> bool:
        """
        :param user_id: User ID, primary key
        :return: Execution result
        """
        query = """
        DELETE FROM user WHERE user_id = %s
        """
        params = (user_id,)
        return self.execute_query(query, params)

    def user_exists(self, user_id: str = None, username: str = None) -> bool:
        """
        :param user_id: User ID, primary key
        :param username: Username
        :return: Result of the query (count)
        """
        params = []
        query = """
        SELECT COUNT(*) as count FROM user
        """
        if user_id:
            query += " WHERE user_id = %s"
            params.append(user_id)
        if username:
            query += " WHERE username = %s"
            params.append(username)
        else:
            return False

        result = self.fetch_query(query, params, single=True)
        return result['count'] > 0

    def update_user(self, user_id: str, data: Dict[str, str]) -> bool:
        query = """
        UPDATE user SET password = %s, status = %s, privilege = %s
        WHERE user_id = %s
        """
        params = tuple(data.values()) + (user_id,)
        return self.execute_query(query, params)

    def get_user_count(self) -> int:
        query = """
        SELECT COUNT(*) as count FROM user
        """
        count = self.fetch_query(query, single=True)
        return count['count']
