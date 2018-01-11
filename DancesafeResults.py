from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt

from secrets import secret_key
from DatabaseMasterList import substancesList, reagentsList

from sqlalchemy.dialects.postgresql import UUID

app = Flask(__name__)
bcrypt = Bcrypt(app)

from alchemy import Colors, Events, ExpectedReactions, MaterialType, \
    ReagentColorList, Reactions, Reagents, Sample, Substances, Survey, \
    TestResults, Questions, Users

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

@app.route('/test_add', methods=['GET', 'POST'])
def test_add():
    if request.method == 'POST':
        users = Users(request.form['username'], request.form['fullname'], request.form['email'], request.form['facebookurl'], request.form['instagram'], request.form['chapter'], request.form['password'])
        session.add(users)
        session.commit()
        print(users)
        return redirect(url_for('show_all'))
    return render_template('adduser.html')


@app.route('/')
def show_all():
    return render_template('show_all.html')


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
            authorUUID = session.query(Users.id).filter(Users.fullname==eachReagent[1]).one()
            newReagent = Reagents(name=eachReagent[0], author=authorUUID, description=eachReagent[2])
            session.add(newReagent)
        session.commit()
        dbreagentList = session.query(
            Reagents.id,
            Reagents.name,
            Reagents.author,
            Reagents.ts,
            Reagents.description)
        for row in session.query(Users).filter(Users.id==authorUUID).all():
            authorName = row.fullname
    return render_template('reagentsindb.html', dbreagentList=dbreagentList, authorName=authorName)



@app.route('/AddMasterSubstanceList', methods=['GET'])
def addmastersubstancelist():
    if request.method == 'GET':
        for eachSubstance in substancesList:
            newSubstance = Substances(name=eachSubstance)
            session.add(newSubstance)
        session.commit()
        dbsubstanceList = session.query(Substances.id, Substances.name)

    return render_template('substancesindb.html', dbsubstanceList=dbsubstanceList)




# @app.route('/add_question', methods=['GET', 'POST'])
# def add_question():
#     eventlist = fetchList(listName='event')
#     userlist = fetchList(listName='user')
#     chapterlist = fetchList(listName='chapter')
#     questionlist = fetchList(listName='question')
#     reagentlist = fetchList(listName='reagent')
#     form = NewQuestion(request.form)
#     if request.method == 'POST':
#         for row in session.query(Questions):
#             print(row)
#         reactionIDList = fetchReagentColorIDs()
#         for i in reactionIDList:
#             print(i)
#         pprint(form.data)
#         return redirect(url_for('add_question'))
#     return render_template(
#         'addquestion.html',
#         chapterlist=chapterlist,
#         eventlist=eventlist,
#         userlist=userlist,
#         questionlist=questionlist,
#         reagentlist=reagentlist,
#         form=form)
#
#
# def fetchReagentColorIDs():
#     """
#     Fetches reagent reaction IDs in the same way the app generates them. By
#     pulling a list of the reagents inside the Reagent table and appending 1,2,3
#     to each reagent generating 3 for each one.
#
#     Returns:
#         reactionIDList: List of IDs that can be called to extract variables.
#     """
#
#     reactionIDList = []
#     reagentList = fetchList(listName='reagent')
#     for eachReagent in reagentList:
#         reactionIDList.append("%sid%i" % (eachReagent, 1))
#         reactionIDList.append("%sid%i" % (eachReagent, 2))
#         reactionIDList.append("%sid%i" % (eachReagent, 3))
#     return reactionIDList
#
#
# @app.route('/')
# def add_data_test2():
#     eventlist = fetchList(listName='event')
#     userlist = fetchList(listName='user')
#     chapterlist = fetchList(listName='chapter')
#     questionlist = fetchList(listName='question')
#     reagentlist = fetchList(listName='reagent')
#     return render_template('survey.html',
#                            reagentlist=reagentlist,
#                            chapterlist=chapterlist,
#                            eventlist=eventlist,
#                            userlist=userlist,
#                            questionlist=questionlist)
#
#
# @app.route('/data_result', methods=['POST', 'GET'])
# def data_result():
#     if request.method == 'POST':
#         result = request.form
#         r = request.form.to_dict()
#         print(r)
#         sampleTableData = SampleTest(
#             chapterName=r['chapterName'],
#             eventid=session.query(EventInfo.id).filter_by(name=r['eventName']),
#             shiftLead=session.query(User.id).filter_by(fullname=r['shiftLead']),
#             tester=session.query(User.id).filter_by(fullname=r['tester']),
#             recorder=session.query(User.id).filter_by(fullname=r['recorder'])
#                 )
#         session.add(sampleTableData)
#         session.commit()
#         sampleUUID = session \
#             .query(SampleTest.id) \
#             .order_by(SampleTest.ts.desc()) \
#             .first()
#         colorIDs = fetchReagentColorIDs()
#         for eachReaction in colorIDs:
#                 reactionData = TestResults(
#                     sampleid=sampleUUID,
#                     testid=eachReaction,
#                     reactioncolor=r[eachReaction]
#                 )
#                 if r[eachReaction]:
#                     session.add(reactionData)
#                     session.commit()
#                     print(r[eachReaction])
#                 else:
#                     pass
#         return render_template("data_result.html", r=r, result=result)


app.secret_key = secret_key

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
