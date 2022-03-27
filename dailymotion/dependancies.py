from redis import Redis
from dailymotion.db import Database
from dailymotion.repositories import Repository
from dailymotion.utils.smtp import SMTPClient
from dailymotion.settings import settings


def get_redis():
    return Redis(host=settings.redis_host, port=int(settings.redis_port))


def get_db():
    return Database(settings.db_uri)


def get_repository():
    db = get_db()
    try:
        yield Repository(db)
    finally:
        db.close()


def get_smtp():
    smtp = SMTPClient(
        host=settings.smtp_host, port=settings.smtp_port, sender=settings.smtp_sender
    )
    return smtp
