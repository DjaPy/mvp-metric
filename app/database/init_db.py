import sqlalchemy

from app.database.db import DATABASE_URL
from app.models import metadata

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)