from sqlalchemy import *

from app.database.conn_root import Base, BaseMixin


class Users(Base, BaseMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    password_re = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    regist_dt = Column(String, nullable=False)
