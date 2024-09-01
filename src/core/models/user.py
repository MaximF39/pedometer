from sqlalchemy import Column, Integer

from core.models import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    step = Column(Integer, nullable=False, default=1)
