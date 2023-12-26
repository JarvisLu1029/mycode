import pymysql
import os
from dotenv import load_dotenv

class SqlQuery():
    def __init__(self, env_path=None):
        load_dotenv(dotenv_path=env_path)

        self.connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT')),
            cursorclass=pymysql.cursors.DictCursor
        )
        self.databases = 'SHOW DATABASES'
    
    def query(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

        return results

    def gen_query(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)

        while True:
            records = cursor.fetchmany(size=100)  # 這裡可以調整每次獲取的記錄數量
            if not records:
                break
            # for record in records:
            yield records

    def get_databases(self):
        with self.connection.cursor() as cursor:
            sql = f'''
                SHOW DATABASES;
                '''
            cursor.execute(sql)
            # results = cursor.fetchall()

        return cursor
