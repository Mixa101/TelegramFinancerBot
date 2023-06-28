from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_FILENAME

engine = create_engine(f"sqlite:///{DB_FILENAME}")
Session = sessionmaker(bind=engine)