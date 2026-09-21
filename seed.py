from sqlite3 import Error
from random import choice
from faker import Faker

from connect import create_connection, database


# Кількість користувачів і завдань
NUMBER_USERS = 10
NUMBER_TASKS = 20


def generate_fake_data(number_users, number_tasks):
    """
    Генерує фейкові дані для користувачів, 
    статусів та завдань за допомогою Faker.

    :param number_users: кількість користувачів
    :param number_tasks: кількість завдань
    :return: users, statuses, tasks
    """

    fake = Faker('uk_UA')

    users = []
    tasks = []
    statuses = ['new', 'in progress', 'completed']

    # ---------------------------------------
    # 1. Генерація користувачів
    # ---------------------------------------

    for _ in range(number_users):

        fullname = fake.name()

        # Унікальна електронна адреса
        email = fake.unique.email()

        users.append((fullname, email))

    # ---------------------------------------
    # 2. Генерація завдань
    # ---------------------------------------

    for _ in range(number_tasks):

        # Генеруємо назву завдання
        title = fake.sentence(nb_words=6)

        # Частина завдань не матиме опису
        description = (
            fake.text(max_nb_chars=200)
            if choice([True, True, False])
            else None
        )

        # ID користувача та статусу додамо пізніше,
        # коли отримаємо їх із бази даних.
        tasks.append((title, description))

    return users, statuses, tasks


def prepare_data(users, statuses, tasks):
    """
    Готує дані до вставки в базу даних.

    :param users: список користувачів
    :param statuses: список статусів
    :param tasks: список завдань
    :return: три списки кортежів
    """

    # Дані для таблиці users
    user_data = [
        (fullname, email)
        for fullname, email in users
    ]

    # Дані для таблиці status
    status_data = [
        (status,)
        for status in statuses
    ]

    # Дані для таблиці tasks
    task_data = [
        (title, description)
        for title, description in tasks
    ]

    return user_data, status_data, task_data


def insert_data(conn, user_data, status_data, task_data):
    """
    Заповнює таблиці users, status і tasks.

    :param conn: підключення до бази даних
    :param user_data: дані користувачів
    :param status_data: дані статусів
    :param task_data: дані завдань
    :return: None
    """

    cur = conn.cursor()

    try:
        # ---------------------------------------
        # 1. Додаємо статуси
        # ---------------------------------------

        sql = """
        INSERT OR IGNORE INTO status (name)
        VALUES (?);
        """

        cur.executemany(sql, status_data)

        # Отримуємо реальні ID статусів із бази
        status_ids = []

        for status_name, in status_data:

            sql = """
            SELECT id
            FROM status
            WHERE name = ?;
            """

            cur.execute(sql, (status_name,))

            status_ids.append(cur.fetchone()[0])

        # ---------------------------------------
        # 2. Додаємо користувачів
        # ---------------------------------------

        user_ids = []

        sql = """
        INSERT INTO users (fullname, email)
        VALUES (?, ?);
        """

        for fullname, email in user_data:

            cur.execute(sql, (fullname, email))

            # Отримуємо ID щойно доданого користувача
            user_ids.append(cur.lastrowid)

        # ---------------------------------------
        # 3. Додаємо завдання
        # ---------------------------------------

        sql = """
        INSERT INTO tasks (
            title,
            description,
            status_id,
            user_id
        )
        VALUES (?, ?, ?, ?);
        """

        for title, description in task_data:

            # Випадково вибираємо реальний ID статусу
            status_id = choice(status_ids)

            # Перевірити SQL-запит № 4.
            # Якщо користувачів більше одного,
            # останнього залишаємо без завдань.
            if len(user_ids) > 1:
                user_id = choice(user_ids[:-1])
            else:
                user_id = choice(user_ids)

            cur.execute(
                sql,
                (title, description, status_id, user_id)
            )

    except Error as e:
        print(f"Помилка заповнення бази даних: {e}")
        raise

    finally:
        cur.close()


# ---------------------------------------
# Запит № 5
# Додати нове завдання конкретному користувачу
# ---------------------------------------

def create_task(conn, task):
    """
    Додає нове завдання в таблицю tasks.

    :param conn: підключення до бази даних
    :param task: кортеж (title, description, status_id, user_id)
    :return: ID нового завдання
    """

    sql = """
    INSERT INTO tasks (
        title,
        description,
        status_id,
        user_id
    )
    VALUES (?, ?, ?, ?);
    """

    cur = conn.cursor()

    try:
        # Додаємо нове завдання
        cur.execute(sql, task)

        # Отримуємо ID нового запису
        task_id = cur.lastrowid

        return task_id

    except Error as e:
        print(f"Помилка додавання завдання: {e}")
        raise

    finally:
        cur.close()


if __name__ == "__main__":

    # Генеруємо та готуємо тестові дані
    users_data, statuses_data, tasks_data = prepare_data(
        *generate_fake_data(NUMBER_USERS, NUMBER_TASKS)
    )

    with create_connection(database) as conn:

        # Заповнюємо базу даних
        insert_data(
            conn,
            users_data,
            statuses_data,
            tasks_data
        )

    print("Базу даних успішно заповнено!")
