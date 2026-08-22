from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean
from database import Base



class NotesDB (Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    version = Column(Integer, default=1)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserDB(Base):
    __tablename__ = 'users'
    id=Column(Integer ,primary_key=True , index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)