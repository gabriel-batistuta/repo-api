import pyodbc
import json

class DataBase():
    def __init__(self, config:dict) -> None:
        self.__server = config['server']
        self.__database = config['database']
        self.__username = config['username']
        self.__password = config['password']
        self.__driver = config['driver']
        self.cursor = self.connect()

    def get_database_config(self):
        return {
            "server": self.__server,
            "database": self.__database,
            "username": self.__username,
            "password": self.__password,
            "driver": self.__driver
        }
    
    def connect(self):
        db_config = self.get_database_config()
        connection_data = f"SERVER={db_config['server']};DATABASE={db_config['database']};UID={db_config['username']};PWD={db_config['password']};DRIVER={{{db_config['driver']}}};"
        
        conn = pyodbc.connect(connection_data)
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        conn.setencoding(encoding='utf-8')

        cursor = conn.cursor()
        return cursor

    def create_table_repositorys(self):
        self.cursor.execute("""
            CREATE TABLE repositorys (
                id BIGSERIAL PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                url TEXT
            );
        """)
        self.cursor.commit()


    def select_table_repositorys(self):
        self.cursor.execute("""SELECT * FROM repositorys;""")
        return self.cursor.fetchall()

    def insert_in_repositorys(self, name, description, url):
        self.cursor.execute("""INSERT INTO repositorys (name, description, url) VALUES (?,?,?);""", (f'{name}',f'{description}',f'{url}'))
        self.cursor.commit()

if __name__ == '__main__':
    with open('config.json','r') as file:
        config = json.load(file)
    db = DataBase(config["postgres"])
    # db.create_table_repositorys()
    # db.insert_in_repositorys('teste', 'teste', 'teste')
    query = db.select_table_repositorys()
    print(query)