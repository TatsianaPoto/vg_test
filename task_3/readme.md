Ожидаемые поля на выходе:
install_date - дата установки когорты
platform - платформа (android/ios)
is_paid - флаг платного трафика
cohort_day - когортный день, считается 24-часовыми интервалам, т.е. [install_time +
N * 24h; install_time + (N + 1) * 24h), где N=0..inf
acc_revenue - аккумулированная по когортным дням сумма платежей когорты в разрезе
install_date, platform, is_paid.
1. Написать SQL-запрос, используя оконные функции, который выведет данные в формате
выше
2. Написать SQL-запрос, не используя оконные функции, который выведет данные в
формате выше



Для получения данных в формате, описанном выше, мы можем использовать оконные функции для вычисления аккумулированной суммы платежей по когортным дням. 
Для этого используем функцию SUM() с оконным смещением ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW, чтобы вычислить сумму платежей от начала когорты 
до текущего дня. Затем присоединяем данные из таблицы users и выполняем группировку по install_date, platform и is_paid. 
Вот SQL-запрос:

SELECT
  users.install_time::date AS install_date,
  users.platform,
  users.is_paid,
  payments.payment_time::date AS cohort_day,
  SUM(payments.revenue) OVER (PARTITION BY users.install_time::date, users.platform, users.is_paid
                              ORDER BY payments.payment_time::date) AS acc_revenue
FROM
  users
LEFT JOIN
  payments
ON
  users.user_id = payments.user_id
ORDER BY
  install_date, platform, is_paid, cohort_day;

  
Производим выборку данных из таблицы users.
Используем левое соединение (LEFT JOIN) с таблицей payments, чтобы включить все записи из users, даже если для них нет соответствующих платежей в таблице payments.
Преобразуем install_time в формат DATE, чтобы получить только дату установки.
Преобразуем payment_time в формат DATE, чтобы получить только дату платежа.
Используем оконную функцию SUM() для вычисления аккумулированной суммы платежей (revenue) по когортным дням (cohort_day) в разрезе install_date, platform и is_paid.
Устанавливаем правильный порядок сортировки результатов с помощью ORDER BY.
Таким образом, данный SQL-запрос выведет данные в требуемом формате, позволяя увидеть аккумулированную сумму платежей когорты по когортным дням для каждой платформы и флага платного трафика.


Чтобы получить данные в ожидаемом формате без использования оконных функций, можно воспользоваться конструкцией JOIN для объединения таблиц 
и подзапросами для вычисления аккумулированной суммы платежей. 
Вот SQL-запрос для получения данных:

SELECT
    u.install_time AS install_date,
    u.platform,
    u.is_paid,
    p.cohort_day,
    COALESCE(SUM(p.revenue) OVER (PARTITION BY u.install_time, u.platform, u.is_paid ORDER BY p.cohort_day), 0) AS acc_revenue
FROM
    users u
LEFT JOIN (
    SELECT
        user_id,
        DATE_TRUNC('day', payment_time) AS cohort_day,
        SUM(revenue) AS revenue
    FROM
        payments
    GROUP BY
        user_id,
        DATE_TRUNC('day', payment_time)
) p ON u.user_id = p.user_id
ORDER BY
    u.install_time,
    u.platform,
    u.is_paid,
    p.cohort_day;

	
В этом запросе, мы используем левое объединение (LEFT JOIN) между таблицами users и подзапросом p, 
который вычисляет сумму платежей для каждого пользователя (user_id) по дням (cohort_day). 
Затем мы используем COALESCE для того, чтобы возвращать 0 в случае, если для данной когорты платежей нет.

Таким образом, результатом будет таблица с полями install_date, platform, is_paid, cohort_day и acc_revenue, 
где acc_revenue представляет собой аккумулированную сумму платежей для каждой когорты в разрезе install_date, platform и is_paid.