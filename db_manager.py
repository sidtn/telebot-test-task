import psycopg2
from settings import *


class DBManager:

    def __init__(self, db_name, db_user, password, host='localhost', port='5432'):
        self.__connect = psycopg2.connect(dbname=db_name,
                                          user=db_user,
                                          password=password,
                                          host=host,
                                          port=port
                                          )
        self.__cursor = self.__connect.cursor()
        print('Connect to base [OK]')

    def create_tables(self):
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, "
                              "user_id BIGINT NOT NULL UNIQUE)")

        self.__cursor.execute("CREATE TABLE IF NOT EXISTS messages (id serial PRIMARY KEY, "
                              "user_id BIGINT NOT NULL, "
                              "last_word TEXT)")
        self.__connect.commit()
        print('table created')

    def check_user(self, user_id):
        self.__cursor.execute(f"SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        return self.__cursor.fetchone()

    def add_user(self, user_id):
        self.__cursor.execute("INSERT INTO users (user_id) VALUES(%s)", (user_id,))
        self.__connect.commit()

    def add_message(self, user_id, last_word):
        self.__cursor.execute("INSERT INTO messages (user_id, last_word) VALUES(%s, %s)", (user_id, last_word,))
        self.__connect.commit()

    def read_last_message(self):
        self.__cursor.execute("SELECT last_word FROM messages ORDER BY id DESC LIMIT 1")
        return self.__cursor.fetchone()

    def get_user_quantity(self):
        self.__cursor.execute("SELECT count(DISTINCT user_id) FROM users")
        return self.__cursor.fetchall()

    def get_tables(self):
        self.__cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
