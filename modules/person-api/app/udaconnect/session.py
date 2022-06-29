from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager

class DbSession():
    __engine = None
    __session = None

    @staticmethod
    def init(databaseUri):
        DbSession.__engine = create_engine(databaseUri, echo = True)
        session_factory = sessionmaker(bind=DbSession.__engine, expire_on_commit=False)
        DbSession.__session = scoped_session(session_factory)
   
    @staticmethod
    @contextmanager
    def session_scope():
        session = DbSession.get_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def get_engine():
        return DbSession.__engine

    @staticmethod
    def get_session():
        return DbSession.__session()