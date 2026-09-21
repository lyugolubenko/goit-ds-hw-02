import sqlite3
from contextlib import contextmanager


# Шлях до файлу бази даних
database = './task_manager.db'


@contextmanager
def create_connection(db_file):
    """
    Контекстний менеджер для безпечного підключення до SQLite.

    :param db_file: шлях до файлу бази даних
    :return: об'єкт з'єднання

    Забезпечує:
    - відкриття підключення;
    - збереження змін після успішної операції;
    - відкат транзакції у випадку помилки;
    - закриття підключення.
    """

    # Створюємо підключення до бази даних
    conn = sqlite3.connect(db_file)

    try:
        # Вмикаємо підтримку зовнішніх ключів - необхідно для ON DELETE CASCADE
        conn.execute("PRAGMA foreign_keys = ON")
        # Передаємо підключення для роботи з базою
        yield conn

    except sqlite3.Error as e:
        # Обробляємо помилки SQLite
        print(f"Помилка SQLite: {e}")
        conn.rollback()     
        # Передаємо помилку далі
        raise

    except Exception:
        # Скасовуємо зміни при помилках
        conn.rollback()
        raise

    else:
        # Зберігаємо зміни після успішного виконання
        conn.commit()

    finally:
        # Закриваємо підключення
        conn.close()