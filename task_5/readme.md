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
