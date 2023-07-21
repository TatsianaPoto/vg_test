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
        SUM(CASE WHEN p.payment_time <= DATE(u.install_time, '+1 day') THEN p.revenue ELSE 0 END) AS revenue_1,
        SUM(CASE WHEN p.payment_time <= DATE(u.install_time, '+3 days') THEN p.revenue ELSE 0 END) AS revenue_3,
        SUM(CASE WHEN p.payment_time <= DATE(u.install_time, '+5 days') THEN p.revenue ELSE 0 END) AS revenue_5,
        SUM(CASE WHEN p.payment_time <= DATE(u.install_time, '+7 days') THEN p.revenue ELSE 0 END) AS revenue_7
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
