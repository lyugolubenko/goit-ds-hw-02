from sqlite3 import Error
from connect import create_connection, database


# ---------------------------------------
# 7. Видалити конкретне завдання
#  
# Використайте DELETE для видалення завдання за його id.
# ---------------------------------------

def delete_task(conn, task_id):
    """
    Видаляє завдання за його ID.

    :param conn: підключення до бази даних
    :param task_id: ID завдання
    :return: кількість видалених записів
    """

    sql = """
    DELETE FROM tasks
    WHERE id = ?;
    """

    cur = conn.cursor()

    try:
        cur.execute(sql, (task_id,))

        return cur.rowcount

    except Error as e:
        print(f"Помилка видалення завдання: {e}")
        raise

    finally:
        cur.close()


# ---------------------------------------
# Каскадне видалення завдань користувача
# ---------------------------------------

def delete_user(conn, user_id):
    """
    Видаляє користувача за його ID.

    Завдання користувача автоматично видаляються
    завдяки ON DELETE CASCADE.

    :param conn: підключення до бази даних
    :param user_id: ID користувача
    :return: кількість видалених користувачів
    """

    sql = """
    DELETE FROM users
    WHERE id = ?;
    """

    cur = conn.cursor()

    try:
        cur.execute(sql, (user_id,))

        return cur.rowcount

    except Error as e:
        print(f"Помилка видалення користувача: {e}")
        raise

    finally:
        cur.close()


if __name__ == "__main__":

    with create_connection(database) as conn:

        # Знаходимо реальний ID першого завдання
        task = conn.execute(
            "SELECT id FROM tasks ORDER BY id LIMIT 1;"
        ).fetchone()

        # ---------------------------------------
        # Виконуємо запит № 7
        # ---------------------------------------

        if task is not None:

            deleted_tasks = delete_task(conn, task[0])

        else:
            deleted_tasks = 0

    print(f"Видалено завдань: {deleted_tasks}")

    # ---------------------------------------
    # Перевірка каскадного видалення
    # ---------------------------------------
    #
    # Функція delete_user() створена вище.
    #
    # Не викликаємо її автоматично,
    # щоб випадково не видалити потрібні дані.

    