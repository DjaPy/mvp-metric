import sqlalchemy

from app.database.db import DATABASE_URL
from app.models import metadata

engine = sqlalchemy.create_engine(DATABASE_URL)

metadata.create_all(engine)
