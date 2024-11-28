import psycopg2

# Підключення до бази даних
connection = psycopg2.connect(
    dbname="locomotive_depot",
    user="user",
    password="password",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()

# Вставка даних
try:
    # Локомотиви
    cursor.execute("""
        INSERT INTO Locomotives (depot, type, year_of_production)
        VALUES
        ('Фастів', 'вантажний', 2010),
        ('Козятин', 'пасажирський', 2012),
        ('П’ятихатки', 'вантажний', 2015);
    """)

    # Бригади
    cursor.execute("""
        INSERT INTO Brigades (phone_number)
        VALUES
        ('0501234567'),
        ('0679876543'),
        ('0633456789');
    """)

    # Робітники
    cursor.execute("""
        INSERT INTO Workers (last_name, first_name, middle_name, brigade_id, is_leader, birth_date)
        VALUES
        ('Іваненко', 'Іван', 'Іванович', 1, TRUE, '1980-01-15'),
        ('Петренко', 'Петро', 'Петрович', 2, FALSE, '1990-07-20'),
        ('Сидоренко', 'Олена', 'Миколаївна', 3, FALSE, '1995-03-10');
    """)

    # Ремонти
    cursor.execute("""
        INSERT INTO Repairs (locomotive_number, type, start_date, days_needed, cost_per_day, brigade_id)
        VALUES
        (1, 'поточний', '2024-11-01', 5, 1000.00, 1),
        (2, 'технічне обслуговування', '2024-11-05', 3, 1200.00, 2),
        (3, 'позаплановий', '2024-11-10', 7, 800.00, 3);
    """)

    connection.commit()
    print("Дані успішно додані.")

except psycopg2.Error as e:
    print(f"Помилка під час виконання запиту: {e}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()
