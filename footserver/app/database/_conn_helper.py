from sqlalchemy.orm import Session
from sqlalchemy.sql import text


class ConnHelper:

    def __init__(self):
        self.db = ""

    @classmethod
    def _create(cls, session: Session, auto_commit=False, **kwargs):
        # 테이블 데이터 적재 전용 함수
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))

        session.add(obj)
        session.flush()

        if auto_commit: session.commit()

        return obj

    @classmethod
    def _get(cls, db, session: Session = None, **kwargs):
        sess = next(db.session()) if not session else session
        query = sess.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one.")
        result = query.first()
        if not session:
            sess.close()
        return result

    @classmethod
    def _filter(cls, db, session: Session = None, **kwargs):
        cond = []

        for key, val in kwargs.items(): cond.append(cls.__create_condition(self=cls, key=key, value=val))

        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def _join(cls, db, sql: str, session: Session = None):
        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.join(text(sql))
        obj._q = query
        return obj

    def __create_condition(self, key, value):
        key = key.split("__")

        if len(key) > 2:
            raise Exception("No 2 more dunders")

        col = getattr(self, key[0])

        if len(key) == 1:
            return col == value
        elif len(key) == 2 and key[1] == 'gt':
            return col > value
        elif len(key) == 2 and key[1] == 'gte':
            return col >= value
        elif len(key) == 2 and key[1] == 'lt':
            return col < value
        elif len(key) == 2 and key[1] == 'lte':
            return col <= value
        elif len(key) == 2 and key[1] == 'in':
            return col.in_(value)
        elif len(key) == 2 and key[1] == 'contains':
            return col.contains(value)
