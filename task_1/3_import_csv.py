import sqlite3
import pandas as pd

# Подключение к базе данных
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Просмотр данных в таблице users
cursor.execute("SELECT * FROM users")
users_data = cursor.fetchall()
users_df = pd.DataFrame(users_data, columns=['user_id', 'install_time', 'platform', 'is_paid'])
print("Данные в таблице users:")
print(users_df)

# Просмотр данных в таблице sessions
cursor.execute("SELECT * FROM sessions")
sessions_data = cursor.fetchall()
sessions_df = pd.DataFrame(sessions_data, columns=['user_id', 'session_time'])
print("\nДанные в таблице sessions:")
print(sessions_df)

# Просмотр данных в таблице payments
cursor.execute("SELECT * FROM payments")
payments_data = cursor.fetchall()
payments_df = pd.DataFrame(payments_data, columns=['user_id', 'payment_time', 'revenue'])
print("\nДанные в таблице payments:")
print(payments_df)

# Сохранение результатов в файл с названием "дата_время.csv"
current_datetime = pd.Timestamp.now().strftime('%Y-%m-%d_%H-%M-%S')
users_df.to_csv(f"{current_datetime}_users.csv", index=False)
sessions_df.to_csv(f"{current_datetime}_sessions.csv", index=False)
payments_df.to_csv(f"{current_datetime}_payments.csv", index=False)

# Закрытие соединения с базой данных
cursor.close()
conn.close()
