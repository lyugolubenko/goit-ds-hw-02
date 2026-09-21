from sqlite3 import Error
from connect import create_connection, database


def create_table(conn, create_table_sql):
    
    """
    Створює таблицю в базі даних SQLite.

    :param conn: об'єкт з'єднання
    :param create_table_sql: SQL-запит CREATE TABLE
    :return: None
    """

    try:
        cur = conn.cursor()

        # Виконуємо SQL-запит створення таблиці
        cur.execute(create_table_sql)

    except Error as e:
        print(f"Помилка створення таблиці: {e}")
        raise

    finally:
        cur.close()


if __name__ == "__main__":

    # ---------------------------------------
    # 1. Створення таблиці users

    # users: id (PK, AUTOINCREMENT),
    # fullname, email (UNIQUE)
    # ---------------------------------------

    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    """

    # ---------------------------------------
    # 2. Створення таблиці status

    # status: id (PK, AUTOINCREMENT),
    # name (UNIQUE)
    # ---------------------------------------

    sql_create_status_table = """
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """

    # ---------------------------------------
    # 3. Створення таблиці tasks

    # tasks: id, title, description,
    # status_id (FK), user_id (FK)
    # ---------------------------------------
    
    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER,
        user_id INTEGER,

        FOREIGN KEY (status_id)
            REFERENCES status(id),

        FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
    );
    """

    # ---------------------------------------
    # 4. Підключення та створення таблиць
    # ---------------------------------------

    with create_connection(database) as conn:

        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_status_table)
        create_table(conn, sql_create_tasks_table)

    print("Таблиці успішно створено.")