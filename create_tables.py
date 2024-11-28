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

# Створення таблиць
try:
    # Локомотиви
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Locomotives (
            id SERIAL PRIMARY KEY,
            registration_number VARCHAR(20) NOT NULL,
            depot VARCHAR(50) NOT NULL,
            type VARCHAR(50) CHECK (type IN ('вантажний', 'пасажирський')) NOT NULL,
            year_of_production INT CHECK (year_of_production > 1900 AND year_of_production <= EXTRACT(YEAR FROM NOW())) NOT NULL
        );
    """)

    # Ремонти
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Repairs (
            id SERIAL PRIMARY KEY,
            locomotive_number INT REFERENCES Locomotives(id) ON DELETE CASCADE,
            type VARCHAR(50) CHECK (type IN ('поточний', 'технічне обслуговування', 'позаплановий')) NOT NULL,
            start_date DATE NOT NULL,
            days_needed INT CHECK (days_needed > 0) NOT NULL,
            cost_per_day NUMERIC(10, 2) CHECK (cost_per_day >= 0) NOT NULL,
            brigade_id INT REFERENCES Brigades(id) ON DELETE SET NULL
        );
    """)

    # Бригади
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Brigades (
            id SERIAL PRIMARY KEY,
            phone_number VARCHAR(15) NOT NULL CHECK (phone_number ~ '^[0-9]{10}$')
        );
    """)

    # Робітники
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Workers (
            id SERIAL PRIMARY KEY,
            last_name VARCHAR(50) NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            middle_name VARCHAR(50),
            brigade_id INT REFERENCES Brigades(id) ON DELETE CASCADE,
            is_leader BOOLEAN NOT NULL DEFAULT FALSE,
            birth_date DATE CHECK (birth_date <= NOW()) NOT NULL
        );
    """)

    connection.commit()
    print("Таблиці успішно створені.")

except psycopg2.Error as e:
    print(f"Помилка під час створення таблиць: {e}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()
