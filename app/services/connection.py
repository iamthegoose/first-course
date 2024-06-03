from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import settings
from sqlalchemy import MetaData

dbcon = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD.get_secret_value()}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(dbcon, echo=True)
metadata_object = MetaData()
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
