from dailymotion.db import Database
from .users import User


class Repository(User):
    def __init__(self, db: Database) -> None:
        User.__init__(self, db)
