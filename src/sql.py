import sqlite3 as sl
import os

from constants import table_file_mapping

con = sl.connect("database.db")

try:
    with con:
        for table_name, file_name in table_file_mapping.items():
            con.execute(f"""
                CREATE TABLE {table_name} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255),
                    price INTEGER,
                    gost TEXT
                );
            """)

            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "data", file_name)
            with open(file_path, "r") as file:
                lines = file.readlines()

            data = [tuple(line.strip().split("|")) for line in lines]
            sql = f"INSERT INTO {table_name} (name, price, gost) VALUES (?, ?, ?)"

            try:
                con.executemany(sql, data)
            except sl.OperationalError:
                print(f"Ошибка при вставке данных в таблицу {table_name}.")
        con.execute("""
                CREATE TABLE profiles (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    telegram INTEGER,
                    name VARCHAR(255),
                    phone_number TEXT,
                    address TEXT
                );
            """)
        con.execute("""
                CREATE TABLE orders (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    type_beef TEXT,
                    name_beef TEXT,
                    quantity INTEGER,
                    date DATETIME,
                    FOREIGN KEY (customer_id) REFERENCES profiles(id)
                );
            """)
        print("База данных успешно создана.")
except sl.OperationalError as er:
    print(f"База данных уже создана. Пропускаем этот этап {er}")
