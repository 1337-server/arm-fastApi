import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

mysql_user = os.getenv("MYSQL_USER", "root")
mysql_password = os.getenv("MYSQL_PASSWORD", "example")
mysql_ip = os.getenv("MYSQL_IP", "127.0.0.1")
DATABASE_URL = 'mysql+mysqlconnector://' + mysql_user + ':' + mysql_password + '@' + mysql_ip + '/arm'

db_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()


def get_db():
    """
    Function to generate db session
    :return: Session
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def init_db():
    try:
        Base.metadata.create_all(bind=db_engine)
    except Exception as e:
        print(e)
        raise e