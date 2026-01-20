from page_analyzer.url_validator import normalize_url
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import OperationalError, IntegrityError
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        yield conn
    except OperationalError as error:
        raise OperationalError(f"Ошибка подключения: {error}") from error
    finally:
        if conn:
            conn.close()


def create_url(url_input):
    success, result = normalize_url(url_input)
    if not success:
        return False, result, None

    try:
        with (get_db_connection() as conn,
              conn.cursor(cursor_factory=RealDictCursor) as curs):
                curs.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING id;",
                    (result,)
                )
                new_id = curs.fetchone()["id"]
                return True, "Страница успешно добавлена", new_id

    except IntegrityError:
        with get_db_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("SELECT id FROM urls WHERE name = %s;", (result,))
            existing_id = curs.fetchone()["id"]
            return False, "Страница уже существует", existing_id


def get_urls():
    with (get_db_connection() as conn,
          conn.cursor(cursor_factory=RealDictCursor) as curs):
            curs.execute("SELECT * FROM urls")
            urls = curs.fetchall()
            return urls


def get_url_by_id(url_id):
    with (get_db_connection() as conn,
          conn.cursor(cursor_factory=RealDictCursor) as curs):
            curs.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            url = curs.fetchone()
            if not url:
                return False
            return url










