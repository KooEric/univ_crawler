from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

engine = create_engine('postgresql://{username}:{password}@{host}:{port}/{db_name}'.format(
    username='postgres', password='postgres', host='127.0.0.1', port='5432', db_name='univ' ))

# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


class Univ(Base):
    __tablename__ = 'univ'
    id = Column(Integer, primary_key=True)
    univ = Column(String(50))
    mojip =Column(String(10))
    major =Column(String(100))
    junhyung = Column(String(100))
    enrollment = Column(Integer)
    competition = Column(Float)

    # Firebird, Oracle에서 PK 생성시 Sequence를 필요로 함(Sequence 생성자 사용)
    # from sqlalchemy import Sequence
    # Column(Integer, Sequence('user_id_seq'), primary_key=True)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.fullname, self.password)

Univ.__tablename__.create(bind=engine, checkfirst=True)

Session = sessionmaker(bind=engine)
session = Session()

univ_list = Univ(
    univ = '가야대학교[본교][경남]',
    mojip="수시",
    major= "간호학과",
    junhyung="학생부위주(교과)>학생부교과(농어촌학생)",
    enrollment=9,
    competition=4.89
)
session.add(univ_list)
session.commit()