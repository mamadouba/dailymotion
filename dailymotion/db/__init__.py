import logging
import psycopg2
from contextlib import contextmanager

logger = logging.getLogger()


class Database:
    def __init__(self, db_uri: str) -> None:
        try:
            logger.info(f"connection to database")
            self.conn = psycopg2.connect(db_uri)
        except Exception as exc:
            logger.exception(f"database connection failed: {str(exc)}")

    def ping(self):
        cur = self.conn.cursor()
        cur.execute("SELECT version();")
        print(cur.fetchone()[0])
        cur.close()

    @contextmanager
    def session(self):
        session = self.conn
        try:
            yield session
        except Exception as exc:
            session.rollback()
            logger.error(f"database operation failed: {str(exc)}")
            raise

    def close(self):
        self.conn.close()

    def fetchone(self, cursor):
        record = cursor.fetchone()
        if not record:
            return {}
        cols = [d[0] for d in cursor.description]
        return dict(zip(cols, record))

    def fetchall(self, cursor):
        cols = [d[0] for d in cursor.description]
        return [dict(zip(cols, record)) for record in cursor.fetchall()]

    def drop_tables(self):
        logger.info("drop tables")
        sql = """
        DROP TABLE users;
        """
        print(sql)
        with self.conn.cursor() as cur:
            cur.execute(sql)
            self.conn.commit()

    def create_tables(self):
        logger.info("create tables")
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            email varchar(100) UNIQUE NOT NULL,
            password_hash varchar(200) NOT NULL,
            status varchar(30) DEFAULT 'new',
            create_date timestamp DEFAULT CURRENT_TIMESTAMP(0)
        );
        """
        print(sql)
        with self.conn.cursor() as cur:
            cur.execute(sql)
            self.conn.commit()
