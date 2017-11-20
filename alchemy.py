import sqlalchemy
from sqlalchemy import create_engine, Boolean, Column, Integer, String, Text, \
    ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID

from wtforms import IntegerField, Form, StringField, validators


from secrets import pgSecret

engine = create_engine(pgSecret, echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()

# Tables


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("uuid_generate_v4()"))
    username = Column(String(30), unique=True, nullable=False)
    fullname = Column(String(100), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    facebookurl = Column(String(50), unique=True, nullable=True)
    chapter = Column(String(50), nullable=True)


class Reactions(Base):
    __tablename__ = 'reactions'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("uuid_generate_v4()"))
    reagent = Column(UUID(as_uuid=True))
    reactionint = Column(Integer(2), unique=False, nullable=False)


class Colors(Base):
    __tablename__ = 'colors'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("uuid_generate_v4()"))
    name = Column(String)
    color = Column(Integer)


# in progress, needs back references
class ReagentColorList(Base):
    __tablename__ = 'colors'

    reaction = Column(UUID(as_uuid=True))
    color = Column(UUID(as_uuid=True))


class NewUser(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    chapter = StringField('Chapter', [validators.Length(min=4, max=40)])


class EventInfo(Base):
    __tablename__ = 'eventinfo'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("uuid_generate_v4()"))
    name = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    region = Column(String(25))


class EventForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=50)])
    year = IntegerField('Year', [validators.Length(min=4, max=4)])
    city = StringField('City', [validators.Length(min=2, max=50)])
    state = StringField('State', [validators.Length(min=2, max=2)])
    region = StringField('Region', [validators.Length(min=2, max=25)])


class Survey(Base):
    __tablename__ = 'survey'

    id = Column(Integer, primary_key=True)
    questionid = Column(Integer, ForeignKey('questions.id'))
    answer = Column(Text)

    def __repr__(self):
        return "<Survey(id='%s', questionid='%s', answer='%s')>" % (
                self.id,
                self.questionid,
                self.answer)


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    detail = Column(Text)


class NewQuestion(Form):
    detail = StringField('detail', [validators.Length(min=4, max=500)])


class Sample(Base):
    __tablename__ = 'sample'

    id = Column(Integer, primary_key=True)
    # make event id back populate from EventInfo Table...
    eventid = Column(UUID, ForeignKey('eventinfo.id'))
    event = relationship('EventInfo', backref='eventinfo')
    surveyid = Column(Integer, ForeignKey('survey.id'))
    survey = relationship('Survey', backref='survey')
    expectedsubstanceid = Column(Integer, ForeignKey('substances.id'))
    groundscorebool = Column(Boolean)

    # same with the User table....
    shiftlead = Column(UUID, ForeignKey('users.id'))
    tester = Column(UUID, ForeignKey('users.id'))
    recorder = Column(UUID, ForeignKey('users.id'))
    testconclusive = Column(Boolean)
    result = Column(Integer, ForeignKey('substances.id'))
    commentbool = Column(Boolean)


class SampleTest(Base):
    __tablename__ = 'sampletest'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    chapterName = Column(String)
    eventid = Column(UUID(as_uuid=True), ForeignKey('eventinfo.id'))
    shiftLead = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    tester = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    recorder = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    ts = Column(DateTime, server_default=sqlalchemy.text("now()"))


class SampleTestForm(Form):
    chapterName = StringField('chapterName')
    eventName = StringField('eventName')
    shiftLead = StringField('shiftLead')
    tester = StringField('tester')
    recorder = StringField('recorder')


class Substances(Base):
    __tablename__ = 'substances'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Tests(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    reagentid = Column(Integer, ForeignKey('reagent.id'))
    colorrank = Column(Integer)


class TestResults(Base):
    __tablename__ = 'testresults'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"))
    sampleid = Column(Integer, ForeignKey('sample.id'))
    testid = Column(UUID(as_uuid=True),
                    ForeignKey('reactionids.id'))
    reactioncolor = Column(String)


class ExpectedReactions(Base):
    __tablename__ = 'expectedreactions'

    id = Column(Integer, primary_key=True)
    testid = Column(Integer, ForeignKey('tests.id'))
    expectedcolor = Column(String)


class Reagent(Base):
    __tablename__ = 'reagent'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("uuid_generate_v4()"))
    name = Column(String)
    author = Column(UUID(as_uuid=True))
    datecreated = Column(DateTime)
    description = Column(Text)
