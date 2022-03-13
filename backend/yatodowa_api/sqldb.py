from flask_sqlalchemy import SQLAlchemy

db = None


def get_db() -> SQLAlchemy:
    global db
    if db is None:
        db = SQLAlchemy()

    return db
