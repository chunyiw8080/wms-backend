import pymysql

from typing import Dict, Any, List
from utils.app_logger import get_logger
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

error_logger = get_logger(logger_name='ErrorLogger', log_file='error.log')

class DatabaseManager():
    def __init__(self):
        self.connection = None

    def __enter__(self):
        self.connection = self.create_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def create_connection(self):
        if not self.connection or not self.connection.open:
            try:
                self.connection = pymysql.connect(
                    host=DB_HOST,
                    user=DB_USER,
                    port=DB_PORT,
                    password=DB_PASSWORD,
                    database=DB_NAME,
                    cursorclass=pymysql.cursors.DictCursor
                )
                # print('Connection established')
            except Exception as e:
                error_logger.error(f'数据库连接错误, {e}')
        return self.connection

    def fetch_query(self, query, params=None, single=False) -> Dict[str, Any] or List[Dict[str, Any]] or None:
        result = None
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, params)
                    if single:
                        result = cursor.fetchone()
                    else:
                        result = cursor.fetchall()
            except Exception as e:
                error_logger.error(f'查询错误, {e}')
        return result

    def execute_query(self, query, params=None) -> bool or None:
        if self.connection:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(query, params)
                    self.connection.commit()
                    return True
            except Exception as e:
                error_logger.error(f'执行异常, {e}')
                self.connection.rollback()
                return None
        else:
            error_logger.error(f'没有建立数据库连接')
        return None

    def close_connection(self):
        if self.connection:
            self.connection.close()


if __name__ == '__main__':
    with DatabaseManager() as db:
        pass
