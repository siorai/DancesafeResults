import sqlalchemy
from sqlalchemy import create_engine, Boolean, Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func, text

from wtforms import RadioField, SelectField, DateTimeField, IntegerField, Form, BooleanField, StringField, PasswordField, validators


from secrets import pgSecret

engine = create_engine(pgSecret, echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine)

session = Session()
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class GUID(TypeDecorator):
        """Platform-independent GUID type.

        Uses PostgreSQL's UUID type, otherwise uses
        CHAR(32), storing as stringified hex values.

        """
        impl = CHAR

        def load_dialect_impl(self, dialect):
            if dialect.name == 'postgresql':
                return dialect.type_descriptor(UUID())
            else:
                return dialect.type_descriptor(CHAR(32))

        def process_bind_param(self, value, dialect):
            if value is None:
                return value
            elif dialect.name == 'postgresql':
                return str(value)
            else:
                if not isinstance(value, uuid.UUID):
                    return "%.32x" % uuid.UUID(value).int
                else:
                    return "%.32x" % value.int

        def process_result_value(self, value, dialect):
            if value is None:
                return value
            else:
                return uuid.UUID(value)


class TestingTesting(Base):
    __tablename__ = 'testingtesting'

    id = Column(GUID, primary_key=True)
    test = Column(String)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    username = Column(String(30), unique=True, nullable=False)
    fullname = Column(String(100), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    facebookurl = Column(String(50), unique=True, nullable=True)
    chapter = Column(String(50), nullable=True)
    

    def __repr__(self):
        return "<User(name='%s', fullname='%s', email='%s', facebookurl='%s', chapter='%s')>" % (
                    self.username, 
                    self.fullname,
                    self.email,
                    self.facebookurl,
                    self.chapter)

    def __init__(self, username=None, fullname=None, email=None, chapter=None, facebookurl=None):
        self.username = username
        self.fullname = fullname
        self.email = email
        self.facebookurl = facebookurl
        self.chapter = chapter


class NewUser(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    chapter = StringField('Chapter', [validators.Length(min=4, max=40)])

class EventInfo(Base):
    __tablename__ = 'eventinfo'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    name = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(2), nullable=False)
    region = Column(String(25))
    #datestart = Column(Date, nullable=False)
    #dateend = Column(Date, nullable=False)

    def __repr__(self):
        return "<EventInfo(name='%s', year='%s', city='%s', state='%s', region='%s')>" % (
                self.name,
                self.year,
                self.city,
                self.state,
                self.region,
                #self.datestart,
                #self.dateend
                )
    
    def __init__(self, name=None, year=None, city=None, state=None, region=None):
        self.name = name
        self.year = year
        self.city = city
        self.state = state
        self.region = region
        #self.datestart = datestart
        #self.dateend = dateend

class EventForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=50)])
    year = IntegerField('Year', [validators.Length(min=4, max=4)])
    city = StringField('City', [validators.Length(min=2, max=50)])
    state = StringField('State', [validators.Length(min=2, max=2, message="Please use abbrevition")])
    region = StringField('Region', [validators.Length(min=2, max=25)])
    #datestart = DateTimeField('datestart')
    #dateend = DateTimeField('dateend')

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

    def __repr__(self):
        return "<Questions(id='%s', detail='%s')>" % (
                self.id,
                self.detail)

    def __init__(self, detail=None):
        self.detail = detail

class NewQuestion(Form):
    detail = StringField('detail', [validators.Length(min=4, max=500)])

class SampleLazyForm(Form):
    chapterName = StringField('chapterName')
    eventName = StringField('eventName')
    shiftLead = StringField('shiftleadName')
    tester = StringField('testerName') 
    recorder = StringField('recorderName')
    substanceType = StringField('substanceType')
    substanceDesc = StringField('sampleDescription')
    substanceExpe = StringField('expectedSubstance')
    substanceOther = StringField('sampleOther')
    marquis1 = StringField('marquis1')
    marquis2 = StringField('marquis2')
    marquis3 = StringField('marquis3')
    mecke1 = StringField('mecke1')
    mecke2 = StringField('mecke2')
    mecke3 = StringField('mecke3')
    mandolin1 = StringField('mandolin1')
    mandolin2 = StringField('mandolin2')
    mandolin3 = StringField('mandolin3')
    simon1 = StringField('simon1')
    simon2 = StringField('simon2')
    simon3 = StringField('simon3')
    liebermann1 = StringField('liebermann1')
    liebermann2 = StringField('liebermann2')
    liebermann3 = StringField('liebermann3')
    froehde1 = StringField('froehde1')
    froehde2 = StringField('froehde2')
    froehde3 = StringField('froehde3')
    folin1 = StringField('folin1')
    folin2 = StringField('folin2')
    folin3 = StringField('folin3')
    ehrlich1 = StringField('ehrlich1')
    ehrlich2 = StringField('ehrlich2')
    ehrlich3 = StringField('ehrlich3')
    conclusivebool = BooleanField('conclusivebool')
    conclusiveresult = StringField('conclusiveSubstance')
    question1 = StringField('question1')
    answer1 = StringField('answer1')
    question2 = StringField('question2')
    answer2 = StringField('answer2')
    question3 = StringField('question3')
    answer3 = StringField('answer3')
    question4 = StringField('question4')
    answer4 = StringField('answer4')
    question5 = StringField('question5')
    answer5 = StringField('answer5')
    question6 = StringField('question6')
    answer6 = StringField('answer6')
    question7 = StringField('question7')
    answer7 = StringField('answer7')
    question8 = StringField('question8')
    answer8 = StringField('answer8')
    question9 = StringField('question9')
    answer9 = StringField('answer9')
    question10 = StringField('question10')
    answer10 = StringField('answer10')
    question11 = StringField('question11')
    answer11 = StringField('answer11')

class SampleLazy(Base):
    __tablename__ = 'samplelazy'

    id = Column(Integer, primary_key=True)
    chapterName = Column(String)
    eventName = Column(String)
    shiftLead = Column(String)
    tester = Column(String)
    recorder = Column(String)
    substanceType = Column(String)
    substanceDesc = Column(Text)
    substanceExpe = Column(String)
    substanceOther = Column(String)
    marquis1 = Column(String)
    marquis2 = Column(String)
    marquis3 = Column(String)
    mecke1 = Column(String)
    mecke2 = Column(String)
    mecke3 = Column(String)
    mandolin1 = Column(String)
    mandolin2 = Column(String)
    mandolin3 = Column(String)
    simon1 = Column(String)
    simon2 = Column(String)
    simon3 = Column(String)
    liebermann1 = Column(String)
    liebermann2 = Column(String)
    liebermann3 = Column(String)
    froehde1 = Column(String)
    froehde2 = Column(String)
    froehde3 = Column(String)
    folin1 = Column(String)
    folin2 = Column(String)
    folin3 = Column(String)
    ehrlich1 = Column(String)
    ehrlich2 = Column(String)
    ehrlich3 = Column(String)
    conclusivebool = Column(Boolean)
    conclusiveresult = Column(String)
    question1 = Column(String)
    answer1 = Column(String)
    question2 = Column(String)
    answer2 = Column(String)
    question3 = Column(String)
    answer3 = Column(String)
    question4 = Column(String)
    answer4 = Column(String)
    question5 = Column(String)
    answer5 = Column(String)
    question6 = Column(String)
    answer6 = Column(String)
    question7 = Column(String)
    answer7 = Column(String)
    question8 = Column(String)
    answer8 = Column(String)
    question9 = Column(String)
    answer9 = Column(String)
    question10 = Column(String)
    answer10 = Column(String)
    question11 = Column(String)
    answer11 = Column(String)
    overallcomments = Column(Text)

    def __init__(self, chapterName=None,
            eventName=None,
            shiftLead=None,
            tester=None,
            recorder=None,
            substanceType=None,
            substanceDesc=None,
            substanceExpe=None,
            substanceOther=None,
            marquis1=None,
            marquis2=None,
            marquis3=None,
            mecke1=None,
            mecke2=None,
            mecke3=None,
            mandolin1=None,
            mandolin2=None,
            mandolin3=None,
            simon1=None,
            simon2=None,
            simon3=None,
            liebermann1=None,
            liebermann2=None,
            liebermann3=None,
            froehde1=None,
            froehde2=None,
            froehde3=None,
            folin1=None,
            folin2=None,
            folin3=None,
            ehrlich1=None,
            ehrlich2=None,
            ehrlich3=None,
            conclusivebool=None,
            conclusiveresult=None,
            question1=None,
            answer1=None,
            question2=None,
            answer2=None,
            question3=None,
            answer3=None,
            question4=None,
            answer4=None,
            question5=None,
            answer5=None,
            question6=None,
            answer6=None,
            question7=None,
            answer7=None,
            question8=None,
            answer8=None,
            question9=None,
            answer9=None,
            question10=None,
            answer10=None,
            question11=None,
            answer11=None):

        self.chapterName = chapterName
        self.eventName = eventName
        self.shiftLead = shiftLead
        self.tester = tester
        self.recorder = recorder
        self.substanceType = substanceType
        self.substanceDesc = substanceDesc
        self.substanceExpe = substanceExpe
        self.substanceOther = substanceOther
        self.marquis1 = marquis1
        self.marquis2 = marquis2
        self.marquis3 = marquis3
        self.mecke1 = mecke1
        self.mecke2 = mecke2
        self.mecke3 = mecke3
        self.mandolin1 = mandolin1
        self.mandolin2 = mandolin2
        self.mandolin3 = mandolin3
        self.simon1 = simon1
        self.simon2 = simon2
        self.simon3 = simon3
        self.liebermann1 = liebermann1
        self.liebermann2 = liebermann2
        self.liebermann3 = liebermann3
        self.froehde1 = froehde1
        self.froehde2 = froehde2
        self.froehde3 = froehde3
        self.folin1 = folin1
        self.folin2 = folin2
        self.folin3 = folin3
        self.ehrlich1 = ehrlich1
        self.ehrlich2 = ehrlich2
        self.ehrlich3 = ehrlich3
        self.conclusivebool = conclusivebool
        self.conclusiveresult = conclusiveresult
        self.question1 = question1
        self.answer1 = answer1
        self.question2 = question2
        self.answer2 = answer2
        self.question3 = question3
        self.answer3 = answer3
        self.question4 = question4
        self.answer4 = answer4
        self.question5 = question5
        self.answer5 = answer5
        self.question6 = question6
        self.answer6 = answer6
        self.question7 = question7
        self.answer7 = answer7
        self.question8 = question8
        self.answer8 = answer8
        self.question9 = question9
        self.answer9 = answer9
        self.question10 = question10
        self.answer10 = answer10
        self.question11 = question11
        self.answer11 = answer11

class Sample(Base):
    __tablename__ = 'sample'
    
    id = Column(Integer, primary_key=True)
    #make event id back populate from EventInfo Table...
    eventid = Column(UUID, ForeignKey('eventinfo.id'))
    event = relationship('EventInfo', backref='eventinfo')
    surveyid = Column(Integer, ForeignKey('survey.id'))
    survey = relationship('Survey', backref='survey')
    expectedsubstanceid = Column(Integer, ForeignKey('substances.id'))
    groundscorebool = Column(Boolean)

    #same with the User table....
    shiftlead = Column(UUID, ForeignKey('users.id'))
    tester = Column(UUID, ForeignKey('users.id'))
    recorder = Column(UUID, ForeignKey('users.id'))
    testconclusive = Column(Boolean)
    result = Column(Integer, ForeignKey('substances.id'))
    commentbool = Column(Boolean)

class SampleTest(Base):
    __tablename__ = 'sampletest'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    chapterName = Column(String)
    eventid = Column(UUID(as_uuid=True), ForeignKey('eventinfo.id'))
    shiftLead = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    tester = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    recorder = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    def __init__(self, chapterName=None, eventName=None, shiftLead=None, tester=None, recorder=None):

        self.chapterName = chapterName
        self.eventName = eventName
        self.shiftLead = shiftLead
        self.tester = tester
        self.recorder = recorder



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

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    sampleid = Column(Integer, ForeignKey('sample.id'))
    testid = Column(Integer, ForeignKey('tests.id'))
    reactioncolor = Column(String)


class ExpectedReactions(Base):
    __tablename__ = 'expectedreactions'
    
    id = Column(Integer, primary_key=True)
    testid = Column(Integer, ForeignKey('tests.id'))
    expectedcolor = Column(String)

class Reagent(Base):
    __tablename__ = 'reagent'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class NewUser(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    chapter = StringField('Chapter', [validators.Length(min=4, max=40)])
