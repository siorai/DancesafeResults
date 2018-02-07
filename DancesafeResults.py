import bcrypt
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask.ext.bcrypt import Bcrypt
from collections import OrderedDict
import webcolors

from flask_cors import CORS

from sqlalchemy import exists

import json

from pprint import pprint

from secrets import secret_key
from DatabaseMasterList import substancesList, reagentsList, materialList, \
    chapterList, userList, colorDict

from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
bcrypt = Bcrypt(app)

from alchemy import Colors, Events, ExpectedReactions, MaterialType, \
    ReagentColorList, Reactions, Reagents, Sample, Substances, Survey, \
    TestResults, Questions, Users, Chapters

from alchemy import session, Base, engine

from pprint import pprint

Base.metadata.create_all(engine)


# def fetchList(listName=None):
#     """
#     Function fetch a list according to listName parameter in order to populate
#     drop down menu in the main survey
#
#     :param listName: name of parameter to be pulled from tables
#         ie event, user, chapter, question
#     :return: list of entries pulled from tables
#     """
#
#     if listName == 'event':
#         eventlist = []
#         for eachEvent in session.query(EventInfo.name, EventInfo.year).all():
#             eventlist.append(eachEvent.name)
#         print(eventlist)
#         return eventlist
#     if listName == 'user':
#         userlist = []
#         for eachUser in session.query(User.fullname).all():
#             userlist.append(eachUser.fullname)
#         print(userlist)
#         return userlist
#     if listName == 'chapter':
#         chapterlist = []
#         for eachChapter in session.query(User.chapter).all():
#             chapterlist.append(eachChapter.chapter)
#         print(chapterlist)
#         return chapterlist
#     if listName == 'question':
#         questionlist = []
#         for eachQuestion in session.query(Questions.detail).all():
#             questionlist.append(eachQuestion)
#         print(questionlist)
#         return questionlist
#     if listName == 'reagent':
#         reagentlist = []
#         for eachReagent in session.query(Reagent.name).all():
#             reagentlist.append(eachReagent.name)
#         print(reagentlist)
#         return reagentlist
#
#
# @app.route('/add_event', methods=['GET', 'POST'])
# def add_event():
#     form = EventForm(request.form)
#     if request.method == 'POST':
#         event = EventInfo(form.name.data,
#                           form.year.data,
#                           form.city.data,
#                           form.state.data,
#                           form.region.data)
#         session.add(event)
#         session.commit()
#         for row in session.query(EventInfo):
#             print(row)
#         return redirect(url_for('add_event'))
#     return render_template('addevent.html', form=form)
#

# @app.route('/add_user', methods=['GET', 'POST'])
# def add_user():
#     form = NewUser(request.form)
#     if request.method == 'POST' and form.validate():
#         user = User(form.username.data, form.name.data, form.email.data,
#                     form.chapter.data)
#         session.add(user)
#         session.commit()
#         for row in session.query(User):
#             print(row)
#         flash('Thank you for creating a user!')
#         return redirect(url_for('add_user'))
#     return render_template('adduser.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def main_app():
    if request.method == 'GET':
        dbchapterList = session.query(Chapters.id, Chapters.name).all()
        pprint(dbchapterList)
        chapterDict = {}
        for id, name in dbchapterList:
            chapterDict[name] = id
        pprint(chapterDict)
        jsonifiedchapterDict = jsonify(chapterDict)
        pprint(jsonifiedchapterDict)
        return render_template('adduser_vuetifytest.html', jsonifiedchapterDict=jsonifiedchapterDict)

@app.route('/test_add', methods=['GET', 'POST'])
def test_add():
    if request.method == 'POST':
        users = Users(request.form['username'],
                      request.form['fullname'],
                      request.form['email'],
                      request.form['facebookurl'],
                      request.form['instagram'],
                      request.form['chapter'],
                      request.form['password'])
        session.add(users)
        session.commit()
        print(users)
        return redirect(url_for('show_all'))
    return render_template('adduser.html')


@app.route('/test', methods=['GET', 'POST'])
def new_survey():
    """
    Currently under development testing handler for the main
    survey portion of the application. Rapidly changes between 
    multiple times between commits and will continue to until the 
    first stable release. 

    Design notes:

    Currently there's console outputs to test the ability of the
    creating and forming the masterDict, an OrderedDict type. 
    As of Python 3.6, Dict types also preserve the order at which
    their entered into the dict, but the specifc PEP relating to it
    specifically mentions that it shouldn't be relied upon, so I'm not.
    
    As of this moment I'm still creating and modifying how I want to 
    form the masterDict inside this URL handler.  

    Since this handler makes several queries to the database, it 
    feels somewhat expensive. Just because the database is hosted 
    for the purpose of this project that doesn't mean I should ignore 
    this vast ineffenciecy.  When I come to the point where I'm happy
    with how the masterDict's data is pulled and formed, I'll be moving
    to its own dedicated function. Then, eventually, it's own class
    and entirely separate file.  

    Overall this is to be considered a database inserter URL. While 
    it does pull some information from the database, the info
    that it requests won't change often enough to need the 
    masterDict to be recreated everytime a new entry is made. 

    As of right now it pulls info from the following tables:
    
    Users: 
        name(String type): to display the name in a drop down
        id(UUID type): to store the UUID for quick entry into the data
            database

    Chapters:
        name(String type): to display the name in the drop down
        id(UUID type): to make storing the UUID for easier.

    Substances:
        name(String type): to display the drop down for each of the 
            substances and displays 
        id: to make storing it easier. 

    returns: basic html page that spits out all of the info that was submitted
        back to the app
    """
    if request.method == 'GET':
        masterDict = dict(eventList={},
                          userList={},
                          chapterList=set(),
                          testing={},
                          materialList=[],
                          colorDict=webcolors.CSS3_NAMES_TO_HEX,
                          reagentsDict={},
                          substancesDict={})
        for row in session.query(Events).order_by(Events.ts):
            masterDict["eventList"]["{} - {}".format(row.name, row.year)] = {"name": "{}".format(row.name),
                                                                             "year": "{}".format(row.year),
                                                                             "id": "{}".format(row.id)}
        for row in session.query(Users):
            masterDict["userList"]["{}".format(row.fullname)] = {"fullname": "{}".format(row.fullname),
                                                                 "id": "{}".format(row.id)}
            masterDict["chapterList"].add(row.chapter)
        for row in session.query(MaterialType).order_by(MaterialType.name):
            masterDict["materialList"].append(row.name)

        dbsubstancesList = session.query(Substances)
        for row in dbsubstancesList:
            masterDict["substancesDict"]["{}".format(row.name)] = row.id
        for row in session.query(Reagents).order_by(Reagents.ts):
            masterDict["reagentsDict"][row.name] = row.id

        pprint(masterDict)
        reagentDict = createImageDict()
        print(reagentDict)
        return render_template('survey-v2.html', masterDict=masterDict, reagentDict=reagentDict)
    if request.method == 'POST':
        dbsurveyList = {
            "chapterid" : request.form['chapter'],
            "eventid" : request.form['event'],
            "shiftleadid" : request.form['shiftLead'],
            "testerid" : request.form['tester'],
            "recorder" : request.form['recorder'],
            "substancetype" : request.form['materialType'],
            "suspectedSubstance" : request.form['suspectedSubstance'],
            "reactions" : {}
        }
        dbsubstancesList = session.query(Reagents)
        for each in dbsubstancesList:
            dbsurveyList["reactions"]["{}".format(each.name)] = request.form["{}Result".format(each.name)]
        return render_template('tobeentered.html', dbsurveyList=dbsurveyList)

@app.route('/api/chapterlist')
def fetch_chapter_list():
    dbchapterList = session.query(Chapters.id, Chapters.name).all()
    pprint(dbchapterList)
    chapterDict = []
    pprint(chapterDict)
    masterDict = dict(eventList={},
                      userList={},
                      chapterList=[],
                      testing={},
                      materialList=[],
                      reagentsDict={},
                      substancesDict={})
    for row in session.query(Events).order_by(Events.ts):
        masterDict["eventList"]["{} - {}".format(row.name, row.year)] = {"name": "{}".format(row.name),
                                                                         "year": "{}".format(row.year),
                                                                         "id": "{}".format(row.id)}
    for row in session.query(Users):
        masterDict["userList"]["{}".format(row.fullname)] = {"fullname": "{}".format(row.fullname)}

    for row in session.query(Chapters):
        masterDict["chapterList"].append(
            {
                "name": "{}".format(row.name),
                "id": "{}".format(row.id)
            }
        )

    for row in session.query(MaterialType).order_by(MaterialType.name):
        masterDict["materialList"].append(row.name)
    return jsonify(masterDict)

@app.route('/add_substance', methods=['GET', 'POST'])
def add_substance():
    if request.method == 'POST':
        substances = Substances(request.form['substance'])
        session.add(substances)
        session.commit()
        print(substances)
        return redirect(url_for('show_all'))
    return render_template('addsubstance.html')


@app.route('/AddReagentList', methods=['GET', 'POST'])
def addreagentlist():
    if request.method == 'GET':
        for eachReagent in reagentsList:
            authorUUID = session.query(Users.id).filter(Users.fullname == eachReagent[1]).one()
            newReagent = Reagents(name=eachReagent[0], author=authorUUID, description=eachReagent[2])
            session.add(newReagent)
        session.commit()
        dbreagentList = session.query(
            Reagents.id,
            Reagents.name,
            Reagents.author,
            Reagents.ts,
            Reagents.description)
        for row in session.query(Users).filter(Users.id == authorUUID).all():
            authorName = row.fullname
        return render_template('reagentsindb.html', dbreagentList=dbreagentList, authorName=authorName)


@app.route('/AddColorReactions', methods=['GET', 'POST'])
def addcolorreactions():
    dbsubstancesList = session.query(Substances)
    dbreactionList = session.query(Reactions)
    dbreagentList = session.query(Reagents).order_by(Reagents.ts)
    dbcolorList = session.query(Colors.id)
    print(type(dbcolorList))
    if request.method == 'GET':
        dbDict = dict()
        for reagents in dbreagentList:
            dbDict.update({reagents.name: {
                "ReagentUUID": reagents.id,
                "ReactionDetails": []
            }
            })
            for eachreaction in dbreactionList.filter(Reactions.reagentid == reagents.id):
                dbDict[reagents.name]["ReactionDetails"].append([eachreaction.id, eachreaction.reactionint])
        print("*****START*****")
        pprint(dbDict)
        print("*****END*****")
        return render_template('addcolorreactions.html',
                               dbsubstancesList=dbsubstancesList,
                               dbreactionList=dbreactionList,
                               dbDict=dbDict)
    for eachReaction in dbreactionList:
        colorname = request.form['ReactionID - {}'.format(eachReaction.id)]
        if colorname == "No Reaction":
            pass
        else:
            if session.query(Colors.name).filter(Colors.name == colorname).scalar() is None:
                addcolor = Colors(name=colorname)
                session.add(addcolor)
                print("You added {}!".format(colorname))
                session.commit()
            else:
                print("Already have it!")
            colorid = session.query(Colors.id).filter(Colors.name == colorname).scalar()
            substanceid = session.query(Substances.id). \
                filter(Substances.name == request.form['substanceName']). \
                scalar()
            reactionid = eachReaction.id
            addreaction = ExpectedReactions(substanceid=substanceid, reactionid=reactionid, colorid=colorid)
            session.add(addreaction)
            session.commit()

    # TODO Make a proper page to verify data entry.


@app.route('/AddReactionList', methods=['GET'])
def addreactionlist():
    if request.method == 'GET':
        for eachReagent in session.query(Reagents):
            newReaction1 = Reactions(reagentid=eachReagent.id, reactionint=0)
            session.add(newReaction1)
            newReaction2 = Reactions(reagentid=eachReagent.id, reactionint=1)
            session.add(newReaction2)
            newReaction3 = Reactions(reagentid=eachReagent.id, reactionint=2)
            session.add(newReaction3)
        session.commit()
        dbreactionList = session.query(Reactions, Reagents). \
            filter(Reactions.reagentid == Reagents.id).all()
        return render_template('dbreactionlist.html', dbreactionList=dbreactionList)


@app.route('/AddMasterSubstanceList', methods=['GET'])
def addmastersubstancelist():
    """
    Adds the substanceList from the DatabaseMasterList into the DB.

    *To be used during initial database creation.

    :return: page that shows all of the substances in the list and their UUIDs.
    """
    if request.method == 'GET':
        for eachSubstance in substancesList:
            newSubstance = Substances(name=eachSubstance)
            session.add(newSubstance)
        session.commit()
        dbsubstanceList = session.query(Substances.id, Substances.name)

        return render_template('substancesindb.html', dbsubstanceList=dbsubstanceList)


@app.route('/AddUserList', methods=['GET'])
def adduserlist():
    """
    Adds the userList from the DatabaseMasterList into the DB.

    *To be used during initial database creation.

    :return: page showing current users in the database.
    """
    if request.method == 'GET':
        for eachUser in userList:
            chapterid = session.query(Chapters.id).filter(Chapters.name == userList[eachUser]['chapter']).scalar()
            newUser = Users(username=userList[eachUser]['username'],
                            fullname=userList[eachUser]['fullname'],
                            email=userList[eachUser]['email'],
                            facebookurl=userList[eachUser]['facebookurl'],
                            instagram=userList[eachUser]['instagram'],
                            chapter=chapterid,
                            _password=userList[eachUser]['Password'])
            session.add(newUser)
        session.commit()
        return render_template('usersindb.html', dbuserList=session.query(Users).all())


@app.route('/AddChapterList', methods=['GET'])
def addchapterlist():
    """
    Adds the chapterList from the DatabaseMasterList into the DB.

    *To be used during initial database creation.

    :return: page showing current chapters in the database.
    """
    if request.method == 'GET':
        for eachChapter in chapterList:
            newChapter = Chapters(name=eachChapter)
            session.add(newChapter)
        session.commit()
        dbchapterList = session.query(Chapters.id, Chapters.name)

        return render_template('chaptersindb.html', dbchapterList=dbchapterList)


@app.route('/AddColorList', methods=['GET'])
def addcolorlist():
    """
    decreciated
    :return:
    """
    if request.method == 'GET':
        for eachColor in colorDict:
            newChapter = Colors(name=eachColor, )
            session.add(newChapter)
        session.commit()
        dbchapterList = session.query(Chapters.id, Chapters.name)
        return render_template('chaptersindb.html', dbchapterList=dbchapterList)


@app.route('/AddMasterMaterialList', methods=['GET'])
def addmastermateriallist():
    """
    Adds the materialList from DatabaseMasterList into the DB.

    *To be used during initial database creation.

    :return: page showing all material types.
    """
    if request.method == 'GET':
        for eachType in materialList:
            newType = MaterialType(name=eachType)
            session.add(newType)
        session.commit()
        dbmateriallist = session.query(MaterialType.id, MaterialType.name).order_by(MaterialType.name)
        return render_template('materialsindb.html', dbmateriallist=dbmateriallist)


# @app.route('/TestingSubmissionResults', methods=['GET', 'POST'])
# def testingSubmissionResults():
#    """
#
#
#    :return: page showing most recently added info
#    """
#    if request.method == 'GET':


def createImageDict():
    """
    Creates the dictionary containing all relevent links to test result images to compare against

    :return: reagentDict
    """
    reagentDict = OrderedDict()
    for eachReagent in reagentsList:
        reagentDict[eachReagent[0]] = {}
        for eachSubstance in substancesList:
            reagentDict[eachReagent[0]][eachSubstance] = (
                "/static/img/reagents/{}/{}_{}.png".format(eachReagent[0], eachReagent[0], eachSubstance)
            )
    return reagentDict

app.secret_key = secret_key

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, ssl_context='adhoc')
