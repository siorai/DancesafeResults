import sqlalchemy
from sqlalchemy import create_engine, Boolean, Column, Integer, String, Text, ForeignKey, Date, DateTime
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


class Reagent(Base):
    __tablename__ = 'reagent'

    id = Column(Integer, primary_key=True)
    name = Column(String)

def fetchList(listName=None):
    """
    Function fetch a list according to listName parameter in order to populate
    drop down menu in the main survey

    :param listName: name of parameter to be pulled from tables
        ie event, user, chapter, question
    :return: list of entries pulled from tables
    """

    if listName == 'reagent':
        reagentlist = []
        for eachReagent in session.query(Reagent.name).all():
            reagentlist.append(eachReagent.name)
        print(reagentlist)
        return reagentlist

def fetchReagentColorIDs():
    """
    Fetches reagent reaction IDs in the same way the app generates them. By
    pulling a list of the reagents inside the Reagent table and appending 1,2,3
    to each reagent generating 3 for each one. 

    Returns:
        reactionIDList: List of IDs that can be called to extract variables.
    """
    
    reactionIDList = []
    reagentList = fetchList(listName='reagent')
    for eachReagent in reagentList:
        reactionIDList.append("%sid%i" % (eachReagent,1))
        reactionIDList.append("%sid%i" % (eachReagent,2))
        reactionIDList.append("%sid%i" % (eachReagent,3))
    return reactionIDList 

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
    detail = StringField('chapterName', [validators.Length(min=4, max=500)])
    print(detail)
    reactionIDList = fetchReagentColorIDs()
    for eachID in reactionIDList:
        eachID = IntegerField(eachID)
        print(eachID)
    Marquisid2 = IntegerField('Marquisid2')
    

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

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
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
    reactionIDList = fetchReagentColorIDs()
    for eachID in reactionIDList:
        eachID = StringField(eachID)
        print(eachID)
    print("Printing Now")
    print(recorder)
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

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
    sampleid = Column(UUID(as_uuid=True), ForeignKey('sampletest.id'))
    testid = Column(String)
    reactioncolor = Column(String)


class ExpectedReactions(Base):
    __tablename__ = 'expectedreactions'
    
    id = Column(Integer, primary_key=True)
    testid = Column(Integer, ForeignKey('tests.id'))
    expectedcolor = Column(String)

class NewUser(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    chapter = StringField('Chapter', [validators.Length(min=4, max=40)])


