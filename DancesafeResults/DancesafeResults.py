import bcrypt
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from collections import OrderedDict, Counter
from itertools import chain
import webcolors
from flask_cors import CORS
import os
import imghdr

from sqlalchemy import exists

import json

from pprint import pprint

from .secrets import secret_key, pgConnection, DBConn, uploadFolder, allowedExtensions
from .DatabaseMasterList import (
    substancesList,
    reagentsList,
    materialList,
    chapterList,
    userList,
    colorDict,
)

import sqlalchemy
from sqlalchemy.orm import class_mapper
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text, select


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = uploadFolder
cors = CORS(app, resources={r"*": {"origins": "*"}})
bcrypt = Bcrypt(app)

from .alchemy import (
    Colors,
    Events,
    ExpectedReactions,
    MaterialType,
    ReagentColorList,
    Reactions,
    Reagents,
    Sample,
    Substances,
    Survey,
    TestResults,
    Questions,
    Users,
    Chapters,
    ApplicationEndPoints,
    ApplicationOrders,
    ApplicationLocationList,
)

from .alchemy import session, Base, engine

from pprint import pprint

from .SQL import demoChart2

Base.metadata.create_all(engine)


def allowedFile(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowedExtensions


@app.route("/api/upload_image_test", methods=["POST"])
def upload_image_test():
    try:
        uploadedImage = request.files["image"]
        print("Hey it worked!!")
        print(type(uploadedImage))
        if uploadedImage and allowedFile(uploadedImage.filename):
            securedFilename = secure_filename(uploadedImage.filename)
            print(securedFilename)
            print(os.path.join(app.config["UPLOAD_FOLDER"], securedFilename))
            uploadedImage.save(
                os.path.join(app.config["UPLOAD_FOLDER"], securedFilename)
            )
        return "Img sent!"
    except:
        print("Nope")
        return "somethin messed up"


@app.route("/vue_chapter_list", methods=["GET"])
def vue_chapter_list():
    if request.method == "GET":
        session.query(Chapters).all()
        vueChapterList = session.query(Chapters).first()
        vueChapterDict = {}
        for eachChapter in vueChapterList:
            vueChapterDict.append(eachChapter)
        pprint(vueChapterDict)
        return jsonify(vueChapterDict)


@app.route("/api/add_sample", methods=["POST"])
def api_add_sample():
    if request.method == "POST":
        newConnection = DBConn()
        currentSession = newConnection.cursor()
        print(request.is_json)
        content = request.get_json()
        print(content)
        eventid = content["eventid"]
        shiftLead = content["shiftLead"]
        tester = content["tester"]
        recorder = content["recorder"]
        typeid = content["typeid"]
        initialSuspect = content["initialSuspect"]
        description = content["description"]
        groundscore = content["groundscore"]
        conclusiveResult = content["conclusiveResult"]
        finalConclusion = content["finalConclusion"]
        acquiredOnSite = content["acquiredOnSite"]
        planToIngest = content["planToIngest"]
        currentSession.execute(
            "INSERT INTO SAMPLE (eventid, shiftlead, tester, recorder, typeid, initialsuspect, description, groundscore, conclusiveresult, finalconclusion, acquiredonsite, plantoingest) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                eventid,
                shiftLead,
                tester,
                recorder,
                typeid,
                initialSuspect,
                description,
                groundscore,
                conclusiveResult,
                finalConclusion,
                acquiredOnSite,
                planToIngest,
            )
        )
        newConnection.commit()
        currentSession.close()
        newConnection.close()
        return "JSON posted"


@app.route("/api/new_event", methods=["POST"])
def api_new_event():
    if request.method == "POST":
        newConnection = DBConn()
        currentSession = newConnection.cursor()
        print(request.is_json)
        content = request.get_json()
        print(content)
        eventName = content["name"]
        eventYear = content["year"]
        eventCity = content["city"]
        eventState = content["state"]
        eventRegion = content["region"]
        eventAuthor = content["author"]
        currentSession.execute(
            "INSERT INTO EVENT (name, year, city, state, region, author) VALUES ('{}', {}, '{}', '{}', '{}', '{}')".format(
                eventName, eventYear, eventCity, eventState, eventRegion, eventAuthor
            )
        )
        newConnection.commit()
        currentSession.close()
        newConnection.close()
        return "JSON posted"


@app.route("/api/demo_chart", methods=["GET"])
def api_demo_chart():
    if request.method == "GET":
        newConnection = DBConn()
        currentSession = newConnection.cursor()
        currentSession.execute(demoChart2)
        jsonifyMe = []
        for each_entry in currentSession.fetchall():
            jsonifyMe.append(each_entry[0])
        piechart = Counter(jsonifyMe)
        print(type(dict(piechart)))
        chartFormat = []
        for key, value in dict(piechart).items():
            chartFormat.append({"label": key, "value": value})
        currentSession.close()
        newConnection.close()
        return jsonify(chartFormat)


@app.route("/api/fetch_substances", methods=["GET"])
def api_fetch_substances():
    if request.method == "GET":
        newConnection = DBConn()
        currentSession = newConnection.cursor()
        currentSession.execute(r"""SELECT s.id, s.name FROM SUBSTANCES as s""")
        jsonifyMe = []
        for each_user in currentSession.fetchall():
            jsonifyMe.append({"id": each_user[0], "name": each_user[1]})
        currentSession.close()
        pgConnection.close()
        return jsonify(jsonifyMe)


@app.route("/api/fetch_events", methods=["GET"])
def api_fetch_events():
    if request.method == "GET":
        newConnection = DBConn()
        currentSession = newConnection.cursor()
        currentSession.execute(
            r"""SELECT EVENT.id, EVENT.name, EVENT.year FROM EVENT"""
        )
        jsonifyMe = []
        for each_user in currentSession.fetchall():
            jsonifyMe.append(
                {
                    "id": each_user[0],
                    "name": ("{} - {}".format(each_user[1], each_user[2])),
                }
            )
        currentSession.close()
        pgConnection.close()
        return jsonify(jsonifyMe)


@app.route("/api/fetch_types", methods=["GET"])
def api_fetch_types():
    if request.method == "GET":
        newConnection = DBConn()
        currentSession = newConnection.cursor()
        currentSession.execute(
            r"""SELECT mt.id, mt.name FROM MATERIALTYPE as mt ORDER BY mt.name"""
        )
        jsonifyMe = []
        for each_user in currentSession.fetchall():
            jsonifyMe.append({"id": each_user[0], "name": each_user[1]})
        currentSession.close()
        pgConnection.close()
        return jsonify(jsonifyMe)


@app.route("/api/fetch_users", methods=["GET"])
def api_fetch_users():
    if request.method == "GET":
        newConnection = DBConn()
        currentSession = newConnection.cursor()
        currentSession.execute(r"""SELECT USERS.id, USERS.fullname FROM USERS""")
        jsonifyMe = []
        for each_user in currentSession.fetchall():
            jsonifyMe.append({"id": each_user[0], "name": each_user[1]})
        currentSession.close()
        pgConnection.close()
        return jsonify(jsonifyMe)


@app.route("/sql_python_test", methods=["GET"])
def sql_python_test():
    pass


@app.route("/fetch_master_dict", methods=["GET"])
def fetch_master_dict():
    if request.method == "GET":
        masterDict = {
            "chapterList": [],
            "endPoints": [],
            "users": [],
            "events": [],
            "menus": {"sidebar": [], "options": [], "footer": []},
        }
        AppOrdersList = attribute_names(ApplicationOrders)
        for each_row in (
            session.query(
                ApplicationOrders.__table__,
                ApplicationEndPoints.__table__,
                ApplicationLocationList.__table__,
            )
            .join(ApplicationEndPoints)
            .join(ApplicationLocationList)
            .filter(ApplicationLocationList.name == "options")
            .order_by(ApplicationOrders.order_int)
            .all()
        ):
            masterDict["menus"]["options"].append(
                {
                    "name": each_row.name,
                    "title": each_row.title,
                    "endpointURL": each_row.endpointURL,
                    "description": each_row.description,
                    "access": each_row.access,
                    "location": each_row.location,
                    "endpoint": each_row.endpoint,
                    "order_int": each_row.order_int,
                }
            )
            masterDict["menus"]["sidebar"].append(each_row)
            print(each_row)
        #        for row in session.query(ApplicationOrders):
        #            print(row.__dict__)
        # masterDict['menus']['options'].append({
        #            print(each_option)
        #            for each_column in AppOrdersList:
        #                masterDict['menus']['options'].append({
        #                    str(each_column): str(each_option.each_column)
        #                    })
        for each_chapter in session.query(Chapters).all():
            masterDict["chapterList"].append(
                {
                    "id": each_chapter.id,
                    "name": each_chapter.name,
                    "facebook": each_chapter.facebook,
                    "twitter": each_chapter.twitter,
                    "snapchat": each_chapter.snapchat,
                    "website": each_chapter.website,
                    "primaryphone": each_chapter.primaryphone,
                    "president": each_chapter.president,
                    "vicepresident": each_chapter.vicepresident,
                    "treasurer": each_chapter.treasurer,
                    "secretary": each_chapter.secretary,
                    "author": each_chapter.author,
                    "ts": each_chapter.ts,
                }
            )
        for each_endpoint in (
            session.query(ApplicationEndPoints)
            .order_by(ApplicationEndPoints.orderint)
            .all()
        ):
            masterDict["endPoints"].append(
                {
                    "name": each_endpoint.name,
                    "title": each_endpoint.title,
                    "endpointURL": each_endpoint.endpointURL,
                    "description": each_endpoint.description,
                    "access": each_endpoint.access,
                    "location": each_endpoint.location,
                    "component": {"name": each_endpoint.endpointURL},
                }
            )
        userattributes = attribute_names(Users)
        for each_user in session.query(Users).all():
            masterDict["users"].append({"name": each_user.fullname, "id": each_user.id})
        for each_event in session.query(Events).all():
            masterDict["events"].append(
                {
                    "name": "{} - {}".format(each_event.name, each_event.year),
                    "id": each_event.id,
                }
            )
        #            masterDict['chapterList'][each_chapter] = {}
        #            for each_column in attribute_names(Chapters):
        #                masterDict['chapterList'][each_chapter].update({
        #                        each_column: "None"})
        #
        pprint(masterDict)
        pprint(attribute_names(Users))
        for each_attribute in attribute_names(Users):
            print("{} is of type: {}".format(each_attribute, type(each_attribute)))
        return jsonify(masterDict)


def attribute_names(cls):
    return [
        prop.key
        for prop in class_mapper(cls).iterate_properties
        if isinstance(prop, sqlalchemy.orm.ColumnProperty)
    ]


@app.route("/test_add", methods=["GET", "POST"])
def test_add():
    if request.method == "POST":
        users = Users(
            request.form["username"],
            request.form["fullname"],
            request.form["email"],
            request.form["facebookurl"],
            request.form["instagram"],
            request.form["chapter"],
            request.form["password"],
        )
        session.add(users)
        session.commit()
        print(users)
        return redirect(url_for("show_all"))
    return render_template("adduser.html")


@app.route("/test", methods=["GET", "POST"])
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
    if request.method == "GET":
        masterDict = dict(eventList={}, userList={}, chapterList={}, testing={})

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
        return render_template(
            "survey-v2.html", masterDict=masterDict, reagentDict=reagentDict
        )
    if request.method == "POST":
        print(request.args.get("key", ""))
        return render_template("addsubstance.html")


@app.route("/add_substance", methods=["GET", "POST"])
def add_substance():
    if request.method == "POST":
        substances = Substances(request.form["substance"])
        session.add(substances)
        session.commit()
        print(substances)
        return redirect(url_for("show_all"))
    return render_template("addsubstance.html")


@app.route("/AddReagentList", methods=["GET", "POST"])
def addreagentlist():
    if request.method == "GET":
        for eachReagent in reagentsList:
            authorUUID = (
                session.query(Users.id).filter(Users.fullname == eachReagent[1]).one()
            )
            newReagent = Reagents(
                name=eachReagent[0], author=authorUUID, description=eachReagent[2]
            )
            session.add(newReagent)
        session.commit()
        dbreagentList = session.query(
            Reagents.id,
            Reagents.name,
            Reagents.author,
            Reagents.ts,
            Reagents.description,
        )
        for row in session.query(Users).filter(Users.id == authorUUID).all():
            authorName = row.fullname
        return render_template(
            "reagentsindb.html", dbreagentList=dbreagentList, authorName=authorName
        )


@app.route("/AddChapterList", methods=["GET"])
def addchapterlist():
    """
    Adds the chapterList from the DatabaseMasterList into the DB.
    *To be used during initial database creation.
    :return: page showing current chapters in the database.
    """
    if request.method == "GET":
        for eachChapter in chapterList:
            newChapter = Chapters(name=eachChapter)
            session.add(newChapter)
        session.commit()
        dbchapterList = session.query(Chapters.id, Chapters.name)

        return render_template("chaptersindb.html", dbchapterList=dbchapterList)


@app.route("/AddColorReactions", methods=["GET", "POST"])
def addcolorreactions():
    dbsubstancesList = session.query(Substances)
    dbreactionList = session.query(Reactions)
    dbreagentList = session.query(Reagents).order_by(Reagents.ts)
    dbcolorList = session.query(Colors.id)
    print(type(dbcolorList))
    if request.method == "GET":
        dbDict = dict()
        for reagents in dbreagentList:
            dbDict.update(
                {reagents.name: {"ReagentUUID": reagents.id, "ReactionDetails": []}}
            )
            for eachreaction in dbreactionList.filter(
                Reactions.reagentid == reagents.id
            ):
                dbDict[reagents.name]["ReactionDetails"].append(
                    [eachreaction.id, eachreaction.reactionint]
                )
        print("*****START*****")
        pprint(dbDict)
        print("*****END*****")
        return render_template(
            "addcolorreactions.html",
            dbsubstancesList=dbsubstancesList,
            dbreactionList=dbreactionList,
            dbDict=dbDict,
        )
    for eachReaction in dbreactionList:
        colorname = request.form["ReactionID - {}".format(eachReaction.id)]
        if colorname == "No Reaction":
            pass
        else:
            if (
                session.query(Colors.name).filter(Colors.name == colorname).scalar()
                is None
            ):
                addcolor = Colors(name=colorname)
                session.add(addcolor)
                print("You added {}!".format(colorname))
                session.commit()
            else:
                print("Already have it!")
            colorid = session.query(Colors.id).filter(Colors.name == colorname).scalar()
            substanceid = (
                session.query(Substances.id)
                .filter(Substances.name == request.form["substanceName"])
                .scalar()
            )
            reactionid = eachReaction.id
            addreaction = ExpectedReactions(
                substanceid=substanceid, reactionid=reactionid, colorid=colorid
            )
            session.add(addreaction)
            session.commit()

    # TODO Make a proper page to verify data entry.


@app.route("/AddReactionList", methods=["GET"])
def addreactionlist():
    if request.method == "GET":
        for eachReagent in session.query(Reagents):
            newReaction1 = Reactions(reagentid=eachReagent.id, reactionint=0)
            session.add(newReaction1)
            newReaction2 = Reactions(reagentid=eachReagent.id, reactionint=1)
            session.add(newReaction2)
            newReaction3 = Reactions(reagentid=eachReagent.id, reactionint=2)
            session.add(newReaction3)
        session.commit()
        dbreactionList = (
            session.query(Reactions, Reagents)
            .filter(Reactions.reagentid == Reagents.id)
            .all()
        )
        return render_template("dbreactionlist.html", dbreactionList=dbreactionList)


@app.route("/AddMasterSubstanceList", methods=["GET"])
def addmastersubstancelist():
    """
    Adds the substanceList from the DatabaseMasterList into the DB.

    *To be used during initial database creation.

    :return: page that shows all of the substances in the list and their UUIDs.
    """
    if request.method == "GET":
        for eachSubstance in substancesList:
            newSubstance = Substances(name=eachSubstance)
            session.add(newSubstance)
        session.commit()
        dbchapterList = session.query(Chapters.id, Chapters.name)
        return render_template("chaptersindb.html", dbchapterList=dbchapterList)


@app.route("/AddMasterMaterialList", methods=["GET"])
def addmastermateriallist():
    """
    Adds the materialList from DatabaseMasterList into the DB.

    *To be used during initial database creation.

    :return: page showing all material types.
    """
    if request.method == "GET":
        for eachType in materialList:
            newType = MaterialType(name=eachType)
            session.add(newType)
        session.commit()
        dbmateriallist = session.query(MaterialType.id, MaterialType.name).order_by(
            MaterialType.name
        )
        return render_template("materialsindb.html", dbmateriallist=dbmateriallist)


def fetchUUID():
    newConnection = DBConn()
    currentSession = newConnection.cursor()
    currentSession.execute("SELECT gen_random_uuid()")
    generatedUUID = currentSession.fetchone()
    currentSession.close()
    newConnection.close()
    return generatedUUID


def createImageDict():
    """
    Creates the dictionary containing all relevent links to test result images to compare against

    :return: reagentDict
    """
    reagentDict = OrderedDict()
    for eachReagent in reagentsList:
        reagentDict[eachReagent[0]] = {}
        for eachSubstance in substancesList:
            reagentDict[eachReagent[0]][
                eachSubstance
            ] = "/static/img/reagents/{}/{}_{}.png".format(
                eachReagent[0], eachReagent[0], eachSubstance
            )
    return reagentDict


app.secret_key = secret_key

if __name__ == "__main__":
    app.run(
        host="192.168.4.1", ssl_context=("../.ssh/fullchain.pem", "../.ssh/privkey.pem")
    )
