from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy

db = None


def get_db() -> SQLAlchemy:
    global db
    if db is None:
        db = SQLAlchemy()

    return db


@contextmanager
def get_session():
    session = get_db().session
    try:
        yield session
        session.commit()
    except BaseException as e:
        session.rollback()
        raise e
