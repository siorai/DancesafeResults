import sqlalchemy
from sqlalchemy import create_engine, Boolean, Column, Integer, String, Text, \
    ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID

from DancesafeResults import bcrypt

from secrets import pgSecret

engine = create_engine(pgSecret, echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()

# Tables


class Colors(Base):
    __tablename__ = 'colors'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    name = Column(String, nullable=False)
    hex = Column(Integer, nullable=True)


class Events(Base):
    __tablename__ = 'event'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    name = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    region = Column(String(25))
    author = Column(UUID(as_uuid=True),
                    ForeignKey('users.id'),
                    nullable=False)
    ts = Column(DateTime, server_default=sqlalchemy.text("now()"))


class ExpectedReactions(Base):
    __tablename__ = 'expectedreactions'

    substanceid = Column(UUID(as_uuid=True),
                         ForeignKey('substances.id'),
                         primary_key=True,
                         nullable=False)
    reactionid = Column(UUID(as_uuid=True),
                        ForeignKey('reactions.id'),
                        primary_key=True,
                        nullable=False)
    colorid = Column(UUID(as_uuid=True),
                     ForeignKey('colors.id'),
                     primary_key=True,
                     nullable=False)


class MaterialType(Base):
    __tablename__ = 'materialtype'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    name = Column(String)
    description = Column(Text)


class ReagentColorList(Base):
    __tablename__ = 'reagentcolorlist'

    reaction = Column(UUID(as_uuid=True),
                      ForeignKey('reactions.id'),
                      primary_key=True,
                      nullable=False)
    color = Column(UUID(as_uuid=True),
                   ForeignKey('colors.id'),
                   primary_key=True,
                   nullable=False)


class Reactions(Base):
    __tablename__ = 'reactions'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    reagentid = Column(UUID(as_uuid=True),
                       ForeignKey('reagent.id'),
                       nullable=False)
    reactionint = Column(Integer, unique=False, nullable=False)


class Reagents(Base):
    __tablename__ = 'reagent'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    name = Column(String)
    author = Column(UUID(as_uuid=True),
                    ForeignKey('users.id'),
                    nullable=False)
    ts = Column(DateTime, server_default=sqlalchemy.text("now()"))
    description = Column(Text)


class Sample(Base):
    __tablename__ = 'sample'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    eventid = Column(UUID(as_uuid=True),
                     ForeignKey('event.id'),
                     nullable=False)
    shiftlead = Column(UUID(as_uuid=True),
                       ForeignKey('users.id'),
                       nullable=False)
    tester = Column(UUID(as_uuid=True),
                    ForeignKey('users.id'),
                    nullable=False)
    recorder = Column(UUID(as_uuid=True),
                      ForeignKey('users.id'),
                      nullable=False)
    ts = Column(DateTime, server_default=sqlalchemy.text("now()"))
    typeid = Column(UUID(as_uuid=True),
                    ForeignKey('materialtype.id'),
                    nullable=False)
    initialsuspect = Column(UUID(as_uuid=True),
                            ForeignKey('substances.id'),
                            nullable=False)
    description = Column(Text)
    groundscore = Column(Boolean)
    conclusiveresult = Column(Boolean)
    finalconclusion = Column(UUID(as_uuid=True),
                             ForeignKey('substances.id'),
                             nullable=False)


class Substances(Base):
    __tablename__ = 'substances'

    # TODO Add author, desc, possibly others

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    name = Column(String)

    def __init__(self, name=None):
        self.name = name


class Survey(Base):
    __tablename__ = 'survey'

    id = Column(Integer, primary_key=True)
    questionid = Column(Integer, ForeignKey('questions.id'))
    answer = Column(Text)


class TestResults(Base):
    __tablename__ = 'testresults'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    sampleid = Column(UUID(as_uuid=True),
                      ForeignKey('sample.id'),
                      nullable=False)
    reactionid = Column(UUID(as_uuid=True),
                        ForeignKey('reactions.id'))
    reactioncolor = Column(UUID(as_uuid=True),
                           ForeignKey('colors.id'))


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    detail = Column(Text)
    author = Column(UUID(as_uuid=True),
                    ForeignKey('users.id'),
                    nullable=False)
    ts = Column(DateTime, server_default=sqlalchemy.text("now()"))


class Users(Base):
    __tablename__ = 'users'

    # TODO Speak with national about additional parameters to exist here

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    username = Column(String(42), unique=True, nullable=False)
    fullname = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    facebookurl = Column(String(50), unique=True, nullable=True)
    instagram = Column(String(50), unique=True, nullable=True)
    chapter = Column(String(50), nullable=True)
    _password = Column(String(128), nullable=False)
    ts = Column(DateTime, server_default=sqlalchemy.text("now()"))

    def __init__(self, username=None, fullname=None, email=None, facebookurl=None, instagram=None,
                 chapter=None, _password=None):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.facebookurl = facebookurl
        self.instagram = instagram
        self.chapter = chapter
        self.password = _password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext).decode('utf-8')


