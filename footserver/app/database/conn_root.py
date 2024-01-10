from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

from sqlalchemy import *

from app.database._conn_helper import *


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):

        # DB 초기화 함수
        database_url = kwargs.setdefault("DB_URL", "")
        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", True)

        self._engine = create_engine(database_url, echo=echo, pool_recycle=pool_recycle, pool_pre_ping=True)

        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            logging.info("DB connected.")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            logging.info("DB disconnected")

    def get_db(self):
        # 요청마다 DB 세션 유지 함수
        if self._session is None:
            raise Exception("must be called 'init_app'")

        db_session = None

        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


class BaseMixin(ConnHelper):
    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        return cls._create(session=session, auto_commit=auto_commit, **kwargs)

    @classmethod
    def get(cls, session: Session = None, **kwargs):
        return cls._get(db=db, session=session, **kwargs)

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        return cls._filter(db=db, session=session, **kwargs)

    def update(self, auto_commit=False, **kwargs):
        result = self._q.update(kwargs)
        if auto_commit:
            self._session.commit()

        return result

    def delete(self, auto_commit: bool = False):
        self._q.delete()
        if auto_commit:
            self._session.commit()

    def first(self):
        result = self._q.first()
        self.close()
        return result

    def all(self, limit: int = 10, offset: int = 0):
        if limit > 0:
            result = self._q.limit(limit).offset(offset).all()
        else:
            result = self._q.all()

        self.close()
        return result

    def count(self):
        result = self._q.count()
        self.close()
        return result

    def order_by(self, *args: str):
        for a in args:
            if a.startswith("-"):
                col_name = a[1:]
                is_asc = False
            else:
                col_name = a
                is_asc = True
            col = self.cls_attr(col_name)
            self._q = self._q.order_by(col.asc()) if is_asc else self._q.order_by(col.desc())
        return self

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()


db = SQLAlchemy()

Base = declarative_base()
