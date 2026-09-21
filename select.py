from sqlite3 import Error
from connect import create_connection, database


def execute_select(conn, sql, params=()):
    """
    Виконує SQL-запит SELECT.

    :param conn: підключення до бази даних
    :param sql: SQL-запит
    :param params: параметри запиту
    :return: список записів
    """

    cur = conn.cursor()

    try:
        # Виконуємо SQL-запит
        cur.execute(sql, params)

        # Отримуємо всі результати
        rows = cur.fetchall()

        return rows

    except Error as e:
        print(f"Помилка виконання SELECT: {e}")
        raise

    finally:
        cur.close()


if __name__ == "__main__":

    with create_connection(database) as conn:

        # ---------------------------------------
        # 1. Отримати всі завдання користувача
        #
        # Використайте SELECT для отримання завдань конкретного 
        # користувача за його user_id
        # ---------------------------------------

        sql = """
        SELECT *
        FROM tasks
        WHERE user_id = ?;
        """

        print("\n1. Завдання користувача:")

        # Беремо ID користувача, який має завдання
        user = conn.execute(
            """
            SELECT user_id
            FROM tasks
            WHERE user_id IS NOT NULL
            LIMIT 1;
            """
        ).fetchone()

        if user is not None:
            print(execute_select(conn, sql, (user[0],)))
        else:
            print("Користувачів із завданнями немає.")

        # ---------------------------------------
        # 2. Завдання зі статусом new
        #
        # Вибрати завдання за певним статусом. Використайте підзапит для вибору
        # завдань з конкретним статусом, наприклад, 'new'
        # ---------------------------------------

        sql = """
        SELECT *
        FROM tasks
        WHERE status_id = (
            SELECT id
            FROM status
            WHERE name = ?
        );
        """

        print("\n2. Завдання зі статусом new:")
        print(execute_select(conn, sql, ("new",)))

        # ---------------------------------------
        # 4. Користувачі без завдань
        # 
        # Отримати список користувачів, які не мають жодного завдання. 
        # Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
        # ---------------------------------------

        sql = """
        SELECT *
        FROM users
        WHERE id NOT IN (
            SELECT user_id
            FROM tasks
            WHERE user_id IS NOT NULL
        );
        """

        print("\n4. Користувачі без завдань:")
        print(execute_select(conn, sql))

        # ---------------------------------------
        # 6. Незавершені завдання
        #
        # Отримати всі завдання, які ще не завершено. 
        # Виберіть завдання, чий статус не є 'завершено'.
        # ---------------------------------------

        sql = """
        SELECT *
        FROM tasks
        WHERE status_id != (
            SELECT id
            FROM status
            WHERE name = ?
        )
        OR status_id IS NULL;
        """

        print("\n6. Незавершені завдання:")
        print(execute_select(conn, sql, ("completed",)))

        # ---------------------------------------
        # 8. Пошук користувачів за email
        #
        # Знайти користувачів з певною електронною поштою. 
        # Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
        # ---------------------------------------

        sql = """
        SELECT *
        FROM users
        WHERE email LIKE ?;
        """

        print("\n8. Пошук користувачів за email:")
        print(execute_select(conn, sql, ("%@example.com",)))

        # ---------------------------------------
        # 10. Кількість завдань за статусами
        #
        # Отримати кількість завдань для кожного статусу.
        # Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами
        # ---------------------------------------

        sql = """
        SELECT
            s.name,
            COUNT(t.id) AS task_count
        FROM status AS s
        LEFT JOIN tasks AS t
            ON s.id = t.status_id
        GROUP BY s.id, s.name;
        """

        print("\n10. Кількість завдань за статусами:")
        print(execute_select(conn, sql))

        # ---------------------------------------
        # 11. Завдання за доменом email
        #
        # Отримати завдання, які призначені користувачам з певною доменною 
        # частиною електронної пошти. 
        # Використайте SELECT з умовою LIKE в поєднанні з JOIN, 
        # щоб вибрати завдання, 
        # призначені користувачам, чия електронна пошта містить певний домен 
        # (наприклад, '%@example.com').
        # ---------------------------------------

        sql = """
        SELECT
            t.*,
            u.email
        FROM tasks AS t
        INNER JOIN users AS u
            ON t.user_id = u.id
        WHERE u.email LIKE ?;
        """

        print("\n11. Завдання користувачів із доменом example.com:")
        print(execute_select(conn, sql, ("%@example.com",)))

        # ---------------------------------------
        # 12. Завдання без опису
        #
        # Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис
        # ---------------------------------------

        sql = """
        SELECT *
        FROM tasks
        WHERE description IS NULL;
        """

        print("\n12. Завдання без опису:")
        print(execute_select(conn, sql))

        # ---------------------------------------
        # 13. Користувачі та завдання in progress
        #
        # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. 
        # Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
        # ---------------------------------------

        sql = """
        SELECT
            u.fullname,
            t.title,
            s.name
        FROM users AS u
        INNER JOIN tasks AS t
            ON u.id = t.user_id
        INNER JOIN status AS s
            ON t.status_id = s.id
        WHERE s.name = ?;
        """

        print("\n13. Завдання у статусі in progress:")
        print(execute_select(conn, sql, ("in progress",)))

        # ---------------------------------------
        # 14. Користувачі та кількість завдань
        #
        # Отримати користувачів та кількість їхніх завдань. 
        # Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
        # ---------------------------------------

        sql = """
        SELECT
            u.fullname,
            COUNT(t.id) AS task_count
        FROM users AS u
        LEFT JOIN tasks AS t
            ON u.id = t.user_id
        GROUP BY u.id, u.fullname;
        """

        print("\n14. Кількість завдань кожного користувача:")
        print(execute_select(conn, sql))