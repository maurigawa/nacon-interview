from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite is an one file database ideal for developement
# and testing purposes. For production, a server database such as
# MySQL or PostgreSQL should be used
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/sql_app.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
