"""
Collection of Object Relational Models to be called on by rest of the app.
Provides overall database schema.
"""
import sqlalchemy
from sqlalchemy import create_engine, Boolean, Column, Integer, String, Text, \
    ForeignKey, DateTime, LargeBinary
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


class Chapters(Base):
    __tablename__ = 'chapters'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    name = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True)
    facebook = Column(String, nullable=True)
    twitter = Column(String, nullable=True)
    snapchat = Column(String, nullable=True)
    website = Column(String, nullable=True)
    primaryphone = Column(String, nullable=True)
    president = Column(UUID(as_uuid=True),
                       ForeignKey('users.id'),
                       nullable=True)
    vicepresident = Column(UUID(as_uuid=True),
                           ForeignKey('users.id'),
                           nullable=True)
    treasurer = Column(UUID(as_uuid=True),
                       ForeignKey('users.id'),
                       nullable=True)
    secretary = Column(UUID(as_uuid=True),
                       ForeignKey('users.id'),
                       nullable=True)
    author = Column(UUID(as_uuid=True),
                    ForeignKey('users.id'),
                    nullable=True)
    ts = Column(DateTime(timezone=True), server_default=sqlalchemy.text("now()"))


class Colors(Base):
    __tablename__ = 'colors'

    # TODO Redo colors table

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    name = Column(String, nullable=False, unique=True)
    hex = Column(String, nullable=True)


class Events(Base):
    __tablename__ = 'event'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    name = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    region = Column(String)
    author = Column(UUID(as_uuid=True),
                    ForeignKey('users.id'),
                    nullable=False)
    ts = Column(DateTime(timezone=True), server_default=sqlalchemy.text("now()"))


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
    ts = Column(DateTime(timezone=True), server_default=sqlalchemy.text("now()"))
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
    ts = Column(DateTime(timezone=True), server_default=sqlalchemy.text("now()"))
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


class ImageComments(Base):
    __tablename__ = 'imagecomments'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    imageid = Column(UUID(as_uuid=True),
                     ForeignKey('testimages.id'),
                     nullable=False)
    reagentid = Column(UUID(as_uuid=True),
                       ForeignKey('reagent.id'),
                       nullable=False)
    details = Column(Text)


class TestImages(Base):
    __tablename__ = 'testimages'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    sampleid = Column(UUID(as_uuid=True),
                      ForeignKey('sample.id'),
                      nullable=False)
    imagefile = Column(LargeBinary)
    description = Column(Text)


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    detail = Column(Text)
    author = Column(UUID(as_uuid=True),
                    ForeignKey('users.id'),
                    nullable=False)
    ts = Column(DateTime(timezone=True), server_default=sqlalchemy.text("now()"))


class Users(Base):
    __tablename__ = 'users'

    # TODO Speak with national about additional parameters to exist here

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    username = Column(String, unique=True, nullable=False)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    facebookurl = Column(String, unique=True, nullable=True)
    instagram = Column(String, unique=True, nullable=True)
    chapter = Column(UUID(as_uuid=True),
                     ForeignKey('chapters.id'),
                     nullable=False)
    _password = Column(String, nullable=False)
    ts = Column(DateTime(timezone=True), server_default=sqlalchemy.text("now()"))

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


