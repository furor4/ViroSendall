from sqlalchemy import create_engine, String, Column, Integer, Boolean, VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base

postgresql_db = 'postgresql://postgres:пароль@localhost:5432/имя базы данных'

engine = create_engine(postgresql_db, echo=True)

Base = declarative_base()


class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True, index=True)
    send_all_text = Column(String, nullable=True)
    per = Column(Integer, default=3600)
    file_id = Column(VARCHAR(250), nullable=True)
    last_message_id = Column(Integer, nullable=True)
    send_status = Column(Boolean, default=False)


class Keyboard(Base):
    __tablename__ = 'keyboard'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(VARCHAR(25))
    url = Column(VARCHAR(250))


Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
