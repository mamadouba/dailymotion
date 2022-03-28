import logging
from typing import List

logger = logging.getLogger()


class User:
    def __init__(self, db) -> None:
        self.db = db

    def create_user(self, **data: dict) -> dict:
        sql = "INSERT INTO users ({0}) VALUES({1}) RETURNING *".format(
            ", ".join(data.keys()), ", ".join(["%s"] * len(data.keys()))
        )
        values = [data[key] for key in data.keys()]
        with self.db.session() as session:
            with session.cursor() as cur:
                cur.execute(sql, values)
                session.commit()
                return self.db.fetchone(cur)

    def get_users(self) -> List[dict]:
        sql = "SELECT * FROM users ORDER BY id;"
        with self.db.session() as session:
            with session.cursor() as cur:
                cur.execute(sql)
                return self.db.fetchall(cur)

    def get_user(self, id: int) -> dict:
        sql = "SELECT * FROM users WHERE id = {0}".format(id)
        with self.db.session() as session:
            with session.cursor() as cur:
                cur.execute(sql)
                return self.db.fetchone(cur)

    def find_user(self, kv: str) -> dict:
        k, v = kv.split("=")
        sql = "SELECT * FROM users WHERE {0} = '{1}'".format(k, v)
        with self.db.session() as session:
            with session.cursor() as cur:
                cur.execute(sql)
                return self.db.fetchone(cur)

    def update_user(self, id: int, **data: dict) -> dict:
        kev = " ".join([f"{k} = '{data[k]}'" for k in data.keys()])
        sql = "UPDATE users SET {0} WHERE id = {1} RETURNING *".format(kev, id)
        with self.db.session() as session:
            with session.cursor() as cur:
                cur.execute(sql)
                session.commit()
                return self.db.fetchone(cur)

    def delete_user(self, id: int):
        sql = "DELETE FROM users WHERE id = {0} RETURNING *".format(id)
        with self.db.session() as session:
            with session.cursor() as cur:
                cur.execute(sql)
                session.commit()
                return self.db.fetchone(cur)
