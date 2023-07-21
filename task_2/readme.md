Изменить код ниже так, чтобы данные из таблицы считывались параллельно. Ваше решение
должно включать функцию previous_date.
CREATE OR REPLACE FUNCTION previous_date(date DATE) RETURNS DATE
 LANGUAGE sql
AS
$$
SELECT date - 1;
$$;
SELECT
 previous_date(date)
FROM
 large_table;
План запроса выше выглядит так:
QUERY PLAN
Seq Scan on large_table
Ожидаемый план запроса:
QUERY PLAN
Gather
 Workers Planned: 3
 -> Parallel Seq Scan on large_table

 

Файл explain.txt - представляет план запроса выполнения запроса, полученный от планировщика запросов PostgreSQL. 
Он описывает, как PostgreSQL планирует выполнение запроса, какие операции будут выполнены и в каком порядке, чтобы получить результат.

Давайте проанализируем код и его план запроса:

Запрос выполняет объединение нескольких таблиц, используя оператор RIGHT JOIN и FULL JOIN.
Ожидается, что выполняется объединение слиянием (Merge Join), что означает, 
что таблицы будут объединены с использованием отсортированных данных для более эффективного выполнения.
Причина использования объединения слиянием (Merge Join) заключается в том, что в плане запроса присутствуют 
операции сортировки (Sort), которые предполагают сортировку данных для более быстрого выполнения объединения.
В запросе выполняется полное объединение (FULL JOIN) для таблиц installs и 
revenue (spend_2021 и spend_2022 отображаются как одна таблица в объединении), 
и результаты будут объединены с таблицей large_table по условиям, заданным в секции Merge Cond.
Объединение выполняется по столбцам install_date, platform, partner и country.
В запросе выполняются операции сортировки (Sort) для таблиц spend_2021, spend_2022 и revenue для оптимизации объединения.
Для таблиц spend_2021 и spend_2022 используется оператор Append, который предполагает объединение данных из нескольких таблиц.
Затем в плане запроса используется операция Gather, что указывает на параллельное выполнение запроса с несколькими рабочими процессами (Workers Planned: 3).
Общая идея плана запроса заключается в объединении данных из нескольких таблиц с использованием сортировки для оптимизации выполнения запроса. 
Планировщик запросов PostgreSQL выбирает оптимальный план выполнения на основе доступных индексов, объема данных и других факторов, 
чтобы минимизировать время выполнения запроса. В этом конкретном случае планировщик запросов решил использовать параллельное выполнение запроса 
для более эффективной обработки данных.

Чтобы выполнить запросы считывания данных параллельно, вы можете использовать функцию parallel в команде SELECT 
и установить соответствующее значение для параметра max_parallel_workers_per_gather. Для этого выполните следующие шаги:

Убедитесь, что параметр max_parallel_workers_per_gather установлен на значение, 
которое позволяет выполнять считывание данных параллельно. 
Это значение можно установить в postgresql.conf или в командной строке при запуске PostgreSQL. 
Например, в файле makefile прописать 
max_parallel_workers_per_gather = 3

CREATE OR REPLACE FUNCTION previous_date(date DATE) RETURNS DATE PARALLEL SAFE
LANGUAGE sql
AS
-- Создаем или обновляем индексы для таблицы large_table, если необходимо
-- Пример индексов для колонок, которые будут использоваться в объединении и фильтрации
CREATE INDEX IF NOT EXISTS idx_install_date ON large_table (install_date);
CREATE INDEX IF NOT EXISTS idx_platform ON large_table (platform);
CREATE INDEX IF NOT EXISTS idx_partner ON large_table (partner);
CREATE INDEX IF NOT EXISTS idx_country ON large_table (country);

-- Устанавливаем режим параллельного сканирования для таблицы large_table
ALTER TABLE large_table SET (parallel_workers = 3);

-- Запрос с использованием параллельного чтения данных из таблицы
-- Для оптимизации запроса, лучше указать условия объединения и фильтрации,
-- которые удовлетворяют индексам, чтобы избежать полного сканирования таблиц.
SELECT
  previous_date(date),
  i.install_date,
  i.platform,
  i.partner,
  i.country,
  i.installs,
  r.net_revenue,
  spend_2021.spend
FROM
  installs i
  LEFT JOIN revenue r ON i.install_date = r.install_date AND i.platform = r.platform AND i.partner = r.partner AND i.country = r.country
  LEFT JOIN (
    SELECT
      spend,
      spend_date,
      platform,
      partner,
      country
    FROM
      spend_2021
    UNION ALL
    SELECT
      spend,
      spend_date,
      platform,
      partner,
      country
    FROM
      spend_2022
  ) spend_2021 ON i.install_date = spend_2021.spend_date AND i.platform = spend_2021.platform AND i.partner = spend_2021.partner AND i.country = spend_2021.country;

  
 В данном коде создается пользовательская функция previous_date, которая принимает аргумент date типа DATE и возвращает DATE. 
 Функция вычисляет предыдущую дату относительно переданной даты, вычитая из нее один день (date - 1).
 
 