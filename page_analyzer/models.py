
from page_analyzer.url_validator import normalize_url
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class DatabaseConnection:
    def __init__(self):
        self.db = os.getenv("DATABASE_URL")
        if not self.db:
            raise ValueError('DATABASE_URL не установлена')

    @contextmanager
    def get_db_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(self.db)
            yield conn
            conn.commit()
        except OperationalError as error:
            if conn:
                conn.rollback()
            raise OperationalError(f"Ошибка подключения: {error}") from error
        finally:
            if conn:
                conn.close()

    def get_cursor(self, query, params=None, fetch_one=False, fetch_all=False):
        with (self.get_db_connection() as conn,
              conn.cursor(cursor_factory=RealDictCursor) as curs):
            curs.execute(query, params or ())
            if fetch_one:
                return curs.fetchone()
            elif fetch_all:
                return curs.fetchall()
            else:
                return curs.rowcount

class URLService:
    def __init__(self):
        self.db = DatabaseConnection()

    def create_url(self, url_input):
        success, normalized_url = normalize_url(url_input)

        if not success:
            return False, normalized_url, None

        existing = self.db.get_cursor(
            "SELECT id FROM urls WHERE name = %s",
            (normalized_url,),
                    fetch_one=True
        )

        if existing:
            return True, "Страница уже существует", existing['id']

        new_url = self.db.get_cursor(
            "INSERT INTO urls (name) VALUES (%s) RETURNING id",
            (normalized_url,),
                    fetch_one=True
        )
        return True, "Страница успешно добавлена", new_url['id']

    def get_urls(self):
        urls = self.db.get_cursor("SELECT * FROM urls", fetch_all=True)
        return urls

    def get_url_by_id(self, url_id):
        url = self.db.get_cursor("SELECT * FROM urls WHERE id = %s", (url_id,), fetch_one=True)
        return url

    def create_check_url(self, url_id):
        pass









