Репозиторий содержит выполненные задания:

 - task_1 - первая задача
 - task_2 - вторая
 - task_3 - третья
 - task_4 - четвертая
 - task_5 - пятая

Пояснения добавлены в файл readme.md



**************

Фидбек по тз:
1. Подсчитаны календарные когортные дни, а не суточные. Использована таблица сессий, которая никак не фигурирует в итоговом запросе :)
2. Файл explain.txt относится только к 5 заданию, но результат здесь получен верный.
3. Сумма должна считаться относительно когортных дней (cohort_day), а не даты платежа. Запрос выведет дублирующуюся атрибуцию, нужно добавить DISTINCT. Дефолтное RANGE-окно уместнее в контексте задачи нежели ROWS-окно. Во второй части задания все равно используется оконная функция. Даже если ее убрать, сделанная модификация запроса не решила бы задачу.
4. Валидация сделана на базовом уровне, не покрывает описания в readme и не находит все заложенные ошибки. Не найдены экстремальные значения, плейсхолдеры, несоответствие campaign_id - campaign_name. Большинство кейсов можно было бы отыскать, если просмотреть таблицу, отсортированную по каждому столбцу отдельно.
5. Не выставлена приоритезация джойнов. Вместо FULL JOIN написан LEFT JOIN. Неправильное условие для LEFT JOIN. FULL JOIN используется для spend_* и revenue, а не installs и revenue, как было описано в readme


```sql
По совокупности выполненного тз отдали предпочтение другому кандидату
```
