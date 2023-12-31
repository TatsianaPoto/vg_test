Восстановите SQL-запрос по его плану. План запроса в приложенном файле explain.txt.

Я очень подробно во второй задаче расписала что в файле, исходя из этого, запрос:

~~~sql
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
~~~


Фидбек от заказчика:

Не выставлена приоритезация джойнов. Вместо FULL JOIN написан LEFT JOIN. 
Неправильное условие для LEFT JOIN. FULL JOIN используется для spend_* и revenue, а не installs и revenue, как было описано в readme


Я не согласна, т.к. не было детализации задания, вместе с тем, я считаю. что:
FULL JOIN и LEFT JOIN (или просто JOIN, что по умолчанию является LEFT JOIN) - это два разных типа соединений (joins) в SQL.

LEFT JOIN:

Возвращает все строки из левой (первой) таблицы и соответствующие строки из правой (второй) таблицы. 
Если нет соответствующих строк в правой таблице, то вместо значений правой таблицы будут выставлены NULL.
При использовании LEFT JOIN, каждая строка из левой таблицы будет участвовать в результирующем наборе, независимо от наличия соответствующих строк в правой таблице.

FULL JOIN:

Возвращает все строки из обеих таблиц и соответствующие строки из друг друга. Если нет соответствующих строк, то будут выставлены NULL.
При использовании FULL JOIN, каждая строка из обеих таблиц будет участвовать в результирующем наборе, даже если нет соответствующих строк в другой таблице.

Если взаменить LEFT JOIN на FULL JOIN в запросе, то произойдет следующее:

 - Все строки из таблицы installs будут включены в результирующий набор, независимо от наличия соответствующих строк в таблицах revenue, spend_2021, spend_2022.
 - Если в таблице revenue нет соответствующей строки для какой-либо строки из installs, вместо значений столбцов из таблицы revenue будут выставлены значения NULL.
 - Аналогично, если в таблице spend_2021 или spend_2022 нет соответствующей строки для какой-либо строки из installs, 
вместо значений столбцов из соответствующей таблицы будут выставлены значения NULL.
 - В результирующем наборе могут появиться дубликаты строк, если для одной строки из installs найдется несколько соответствующих строк в таблицах 
revenue, spend_2021, spend_2022.

В целом, использование FULL JOIN расширяет объем данных, возвращаемых из таблиц, и может привести к возникновению дублирующихся строк. 
Если это не является ожидаемым поведением для запроса, то можно оставить LEFT JOIN, чтобы включить только соответствующие строки из таблиц: 
revenue, spend_2021, spend_2022, и не включать дубликаты.
