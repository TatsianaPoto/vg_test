Необходимо написать SQL-запрос, который будет выводить следующую информацию:

~~~sql
install_date - дата установки когорты
installs - количество установок в install_date
purchases - количество платежей за все время
buyers - количество плательщиков в за все время
revenue - сумма платежей за все время
revenue_1 - сумма платежей, совершенных когортой до первого когортного дня (N<=1)
revenue_3 - сумма платежей, совершенных когортой до третьего когортного дня
revenue_5 - сумма платежей, совершенных когортой до пятого когортного дня
revenue_7 - сумма платежей, совершенных когортой до седьмого когортного дня
Примечание: Когортный день считается 24-часовыми интервалам, т.е. [install_time + N *
24h; install_time + (N + 1) * 24h), где N=0..inf
~~~


Для решения этой задачи, нам необходимо выполнить несколько шагов:

 - Вычислить когортный день для каждой установки из таблицы "users".
 - Вычислить количество установок, платежей, и плательщиков за все время для каждой когорты.
 - Вычислить сумму платежей за все время для каждой когорты.
 - Вычислить сумму платежей, совершенных когортой до первого, третьего, пятого и седьмого когортного дня для каждой когорты.
 - Ниже представлен SQLite-запрос, который выполняет все эти шаги:

~~~sql
WITH cohort_data AS (
    SELECT
        user_id,
        install_time AS install_date,
        strftime('%Y-%m-%d', install_time, 'start of day') AS cohort_day
    FROM
        users
),
cohort_summary AS (
    SELECT
        cohort_day,
        COUNT(DISTINCT user_id) AS installs,
        SUM(CASE WHEN payments.user_id IS NOT NULL THEN 1 ELSE 0 END) AS purchases,
        SUM(CASE WHEN payments.user_id IS NOT NULL THEN revenue ELSE 0 END) AS revenue,
        SUM(CASE WHEN payments.user_id IS NOT NULL THEN 1 ELSE 0 END) AS buyers,
        SUM(CASE WHEN cohort_day = install_date THEN revenue ELSE 0 END) AS revenue_1,
        SUM(CASE WHEN cohort_day <= DATE(install_date, '+3 days') THEN revenue ELSE 0 END) AS revenue_3,
        SUM(CASE WHEN cohort_day <= DATE(install_date, '+5 days') THEN revenue ELSE 0 END) AS revenue_5,
        SUM(CASE WHEN cohort_day <= DATE(install_date, '+7 days') THEN revenue ELSE 0 END) AS revenue_7
    FROM
        cohort_data
    LEFT JOIN
        payments ON cohort_data.user_id = payments.user_id
    GROUP BY
        cohort_day
)
SELECT
    cohort_summary.*,
    strftime('%Y-%m-%d', install_time, 'start of day') AS install_date
FROM
    users
LEFT JOIN
    cohort_summary ON strftime('%Y-%m-%d', users.install_time, 'start of day') = cohort_summary.cohort_day
ORDER BY
    install_date;
~~~	
	
 - В этом запросе я использую WITH-клаузу для создания двух временных таблиц - cohort_data и cohort_summary. 
 - Первая таблица cohort_data вычисляет когортный день для каждой установки. 
 - Вторая таблица cohort_summary считает необходияе данные для каждой когорты. 
 - Затем я объединяем таблицы users и cohort_summary, чтобы получить окончательный результат.



НО, т.к. я предпочитаю работать с Python и разработку в VSCode:

1. Создам пустую бд и добавлю три пустые таблицы:

~~~sql
таблица: users
поле: user_id UUID
поле: install_time TIMESTAMP
поле: platform TEXT 
поле: is_paid BOOLEAN
~~~

~~~sql
таблица: sessions
поле: user_id UUID
поле: session_time TIMESTAMP
~~~

~~~sql
таблица: payments
поле: user_id UUID
поле: payment_time TIMESTAMP
поле: revenue NUMERIC
~~~

для создания бд с таблицами необходимо запустить скрипт: python 1_sql_db.py


2. Добавлю 1000 рандомных значений в каждую из таблиц исходя из структуры данных описанных выше.

Для этого необходимо запустить скрипт: python 2_load.py

3. Подключусь к бд и проверю, что есть данные, а также выгружу данные в csv.

для проверки и выгрузки необходимо запустить скрипт: python 3_import_csv.py

~~~sql
результатом выполения скрипта является три файла csv:
2023-07-21_12-26-24_payments.csv
2023-07-21_12-26-24_sessions.csv
2023-07-21_12-26-24_users.csv
~~~

4. Для решения первой задачи необходиом запустить скрпит: python 4_task_1.py

	В этом коде я создала две функции: 

	execute_sql_query, которая выполняет SQL-запрос и возвращает результат. 

	get_cohort_revenue, которая формирует и выполняет SQL-запрос для получения информации о когортном доходе. 

	После выполнения запроса результаты выводятся в консоль и сохраняется в файл cohort_revenue.csv в текущей директории.

	Файл будет содержать данные в формате CSV, где каждая строка будет соответствовать одной когорте и значениям столбцов 
~~~sql
install_date, installs, buyers, purchases, revenue, revenue_1, revenue_3, revenue_5, revenue_7.
~~~

фидбек от заказчика:
Подсчитаны календарные когортные дни, а не суточные. Использована таблица сессий, которая никак не фигурирует в итоговом запросе

Исправленный итоговый запрос 4_task_1.py будет выглядить так:
~~~sql
import sqlite3
import csv

def execute_sql_query(query):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_cohort_revenue():
    query = '''
    SELECT
        u.install_time AS install_date,
        COUNT(DISTINCT u.user_id) AS installs,
        COUNT(DISTINCT p.user_id) AS buyers,
        COUNT(p.revenue) AS purchases,
        SUM(p.revenue) AS revenue,
        SUM(CASE WHEN p.payment_time <= strftime('%s', u.install_time) + 1 * 24 * 60 * 60 THEN p.revenue ELSE 0 END) AS revenue_1,
        SUM(CASE WHEN p.payment_time <= strftime('%s', u.install_time) + 3 * 24 * 60 * 60 THEN p.revenue ELSE 0 END) AS revenue_3,
        SUM(CASE WHEN p.payment_time <= strftime('%s', u.install_time) + 5 * 24 * 60 * 60 THEN p.revenue ELSE 0 END) AS revenue_5,
        SUM(CASE WHEN p.payment_time <= strftime('%s', u.install_time) + 7 * 24 * 60 * 60 THEN p.revenue ELSE 0 END) AS revenue_7
    FROM
        users u
    LEFT JOIN
        sessions s ON u.user_id = s.user_id
    LEFT JOIN
        payments p ON u.user_id = p.user_id
    GROUP BY
        u.install_time
    ORDER BY
        u.install_time;
    '''
    return execute_sql_query(query)

if __name__ == "__main__":
    results = get_cohort_revenue()

    with open('cohort_revenue.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['install_date', 'installs', 'buyers', 'purchases', 'revenue', 'revenue_1', 'revenue_3', 'revenue_5', 'revenue_7'])
        csvwriter.writerows(results)
~~~

Т.е. в этом коде я заменила DATE(u.install_time, '+1 day') на strftime('%s', u.install_time) + 1 * 24 * 60 * 60, чтобы вычислить когортный день в секундах и проверить, что p.payment_time меньше или равно этому значению. Аналогичные изменения я сделала и для других когортных дней (revenue_3, revenue_5, revenue_7).

