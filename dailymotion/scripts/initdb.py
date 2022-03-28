#!/bin/env python3
import os
import logging
import psycopg2 as pg

logger = logging.getLogger(__name__)

def connect_db():
    logger.info("connect to database")
    conn = pg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    return conn


def drop_tables():
    conn = connect_db()
    conn.autocommit = True
    cur = conn.cursor()

    logger.info("drop tables")
    sql = """
    DROP TABLE IF EXISTS users;
    """
    print(sql)
    cur.execute(sql)
    cur.close()
    conn.close()


def create_tables():
    conn = connect_db()
    conn.autocommit = True
    cur = conn.cursor()

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
    cur.execute(sql)
    cur.close()
    conn.close()


if __name__ == "__main__":
    drop_tables()
    create_tables()