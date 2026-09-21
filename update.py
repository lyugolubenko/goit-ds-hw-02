from sqlite3 import Error
from connect import create_connection, database


# ---------------------------------------
# Спільна функція для виконання UPDATE
# ---------------------------------------

def execute_update(conn, sql, parameters):
    """
    Виконує SQL-запит UPDATE.

    :param conn: підключення до бази даних
    :param sql: SQL-запит
    :param parameters: параметри запиту
    :return: кількість оновлених записів
    """

    cur = conn.cursor()

    try:
        # Виконуємо SQL-запит із параметрами
        cur.execute(sql, parameters)

        # Повертаємо кількість оновлених записів
        return cur.rowcount

    except Error as e:
        print(f"Помилка виконання UPDATE: {e}")
        raise

    finally:
        # Закриваємо курсор
        cur.close()


# ---------------------------------------
# 3.  Оновлення статусу завдання
#
# Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
# ---------------------------------------

def update_task_status(conn, status_id, task_id):
    """
    Оновлює статус конкретного завдання.
    """

    sql = """
    UPDATE tasks
    SET status_id = ?
    WHERE id = ?;
    """

    return execute_update(
        conn,
        sql,
        (status_id, task_id)
    )


# ---------------------------------------
# 9. Оновлення імені користувача
# 
# Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
# ---------------------------------------

def update_user_name(conn, fullname, user_id):
    """
    Оновлює повне ім'я користувача.
    """

    sql = """
    UPDATE users
    SET fullname = ?
    WHERE id = ?;
    """

    return execute_update(
        conn,
        sql,
        (fullname, user_id)
    )


if __name__ == "__main__":

    with create_connection(database) as conn:

        # Отримуємо ID першого завдання
        task = conn.execute(
            "SELECT id FROM tasks ORDER BY id LIMIT 1;"
        ).fetchone()

        # Отримуємо ID статусу in progress
        status = conn.execute(
            "SELECT id FROM status WHERE name = ?;",
            ("in progress",)
        ).fetchone()

        # Отримуємо ID першого користувача
        user = conn.execute(
            "SELECT id FROM users ORDER BY id LIMIT 1;"
        ).fetchone()

        # ---------------------------------------
        # Виконуємо запит № 3
        # ---------------------------------------

        if task is not None and status is not None:

            updated_tasks = update_task_status(
                conn,
                status[0],
                task[0]
            )

        else:
            updated_tasks = 0

        # ---------------------------------------
        # Виконуємо запит № 9
        # ---------------------------------------

        if user is not None:

            updated_users = update_user_name(
                conn,
                "Людмила Петренко",
                user[0]
            )

        else:
            updated_users = 0

    # Виводимо результат після збереження змін
    print(f"Оновлено завдань: {updated_tasks}")
    print(f"Оновлено користувачів: {updated_users}")