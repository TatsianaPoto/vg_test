import sqlite3

# Подключение к базе данных (если файл не существует, то он будет создан)
conn = sqlite3.connect('data.db')

# Создание объекта курсора
cursor = conn.cursor()

# SQL-запрос для создания таблицы users
create_table_users = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        install_time TIMESTAMP,
        platform TEXT,
        is_paid BOOLEAN
    )
"""

# SQL-запрос для создания таблицы sessions
create_table_sessions = """
    CREATE TABLE IF NOT EXISTS sessions (
        user_id TEXT,
        session_time TIMESTAMP
    )
"""

# SQL-запрос для создания таблицы payments
create_table_payments = """
    CREATE TABLE IF NOT EXISTS payments (
        user_id TEXT,
        payment_time TIMESTAMP,
        revenue NUMERIC
    )
"""

# Выполнение SQL-запросов для создания таблиц
cursor.execute(create_table_users)
cursor.execute(create_table_sessions)
cursor.execute(create_table_payments)

# Подтверждение изменений в базе данных
conn.commit()

# Закрытие соединения с базой данных
cursor.close()
conn.close()
