import psycopg2

queries = {
    "Вантажні локомотиви": """
        SELECT * FROM Locomotives WHERE type = 'вантажний' ORDER BY year_of_production;
    """,
    "Кінцева дата ремонту": """
        SELECT locomotive_number, (start_date + days_needed * INTERVAL '1 day') AS end_date
        FROM Repairs;
    """,
    "Кількість ремонтів по бригадах": """
        SELECT brigade_id, COUNT(*) AS repair_count
        FROM Repairs
        GROUP BY brigade_id;
    """,
    "Повна вартість ремонту": """
        SELECT locomotive_number, SUM(days_needed * cost_per_day) AS total_cost
        FROM Repairs
        GROUP BY locomotive_number;
    """,
    "Типи ремонтів по бригадах": """
        SELECT brigade_id, type, COUNT(*) AS type_count
        FROM Repairs
        GROUP BY brigade_id, type;
    """,
    "Локомотиви обраного депо": """
        SELECT * FROM Locomotives WHERE depot = 'Фастів';
    """
}

connection = psycopg2.connect(
    dbname="locomotive_depot",
    user="user",
    password="password",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

try:
    for description, query in queries.items():
        print(f"\n{description}:")
        if "%s" in query:
            cursor.execute(query, ('Фастів',))
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
finally:
    cursor.close()
    connection.close()
