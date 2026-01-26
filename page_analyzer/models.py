
from page_analyzer.url_validator import normalize_url
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from page_analyzer.parser_url import get_data

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class DatabaseConnection:
    def __init__(self):
        self.db = os.getenv("DATABASE_URL")
        if not self.db:
            raise ValueError("DATABASE_URL не установлена")

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
            return True, "Страница уже существует", existing["id"]

        new_url = self.db.get_cursor(
            "INSERT INTO urls (name) VALUES (%s) RETURNING id",
            (normalized_url,),
                    fetch_one=True
        )
        return True, "Страница успешно добавлена", new_url["id"]

    def get_urls(self):
        urls = self.db.get_cursor("SELECT * FROM urls", fetch_all=True)
        return urls

    def get_url_by_id(self, url_id):
        url = self.db.get_cursor(
            "SELECT * FROM urls WHERE id = %s",
            (url_id,), fetch_one=True)
        return url

    def create_check_url(self, url_id):
        url = self.get_url_by_id(url_id)
        if not url:
            return False

        url_data = get_data(url["name"])
        if not url_data or url_data["status_code"] >= 500:
            return False

        self.db.get_cursor(
            """
            INSERT INTO url_checks (url_id, status_code, h1, title, description)
            VALUES (%s, %s, %s, %s, %s) RETURNING id, created_at
            """,
            (
                url_id, url_data["status_code"],
                url_data["h1"],
                url_data["title"],
                url_data["description"]),
            fetch_one=True
        )
        return True

    def get_checks_url(self, url_id):
        checks_url = self.db.get_cursor(
            """
            SELECT
                id,
                status_code,
                h1,
                title,
                description,
                created_at
            FROM url_checks
            WHERE url_id = %s
            ORDER BY created_at DESC
            """,
            (url_id,),
            fetch_all=True)

        return checks_url or []

    def get_urls_with_last_check(self):
        return self.db.get_cursor("""
                SELECT DISTINCT ON (urls.id)
                    urls.id,
                    urls.name,
                    urls.created_at,
                    checks.created_at as last_check_at,
                    checks.status_code
                FROM urls
                LEFT JOIN LATERAL (
                    SELECT status_code, created_at
                    FROM url_checks 
                    WHERE url_id = urls.id
                    ORDER BY created_at DESC
                    LIMIT 1
                ) checks ON true
                ORDER BY urls.id
            """, fetch_all=True)














