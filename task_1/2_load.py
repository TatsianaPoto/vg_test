import sqlite3
import uuid
import random
from datetime import datetime, timedelta

# Подключение к базе данных
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Заполнение таблицы users
def generate_random_user():
    user_id = uuid.uuid4()
    install_time = datetime(2022, random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59))
    platform = random.choice(['Android', 'iOS'])
    is_paid = random.choice([True, False])
    return user_id, install_time, platform, is_paid

for _ in range(1000):
    user_id, install_time, platform, is_paid = generate_random_user()
    cursor.execute("INSERT INTO users (user_id, install_time, platform, is_paid) VALUES (?, ?, ?, ?)",
                   (str(user_id), install_time, platform, is_paid))

# Заполнение таблицы sessions
def generate_random_session():
    cursor.execute("SELECT user_id FROM users")
    user_ids = cursor.fetchall()
    user_id = random.choice(user_ids)[0]
    session_time = datetime(2022, random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59))
    return user_id, session_time

for _ in range(1000):
    user_id, session_time = generate_random_session()
    cursor.execute("INSERT INTO sessions (user_id, session_time) VALUES (?, ?)",
                   (str(user_id), session_time))

# Заполнение таблицы payments
def generate_random_payment():
    cursor.execute("SELECT user_id FROM users")
    user_ids = cursor.fetchall()
    user_id = random.choice(user_ids)[0]
    payment_time = datetime(2022, random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59))
    revenue = random.randint(1, 1000)
    return user_id, payment_time, revenue

for _ in range(1000):
    user_id, payment_time, revenue = generate_random_payment()
    cursor.execute("INSERT INTO payments (user_id, payment_time, revenue) VALUES (?, ?, ?)",
                   (str(user_id), payment_time, revenue))

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
cursor.close()
conn.close()

print("Данные успешно заполнены в таблицы users, sessions и payments.")
