from flask import Flask, flash, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap

from wtforms import Form, BooleanField, StringField, PasswordField, validators


#  import MySQLdb

from Alchemy import *

app = Flask(__name__)

#db = MySQLdb.connect(
#        host="localhost",
#        user="root",
#        passwd="dancesafedancesafe",
#        db="DS_Testing"
#        )

# cur = db.cursor()

Base.metadata.create_all(engine)



@app.route('/')
def hello_world():
    return 'Hello World!'

def fetchList(listName=None):
    if listName == 'event':
        eventlist = []
        for eachEvent in session.query(EventInfo.name, EventInfo.year):
            eventlist.append(eachEvent)
        print(eventlist)
        return eventlist
    if listName == 'user':
        userlist = []
        for eachUser in session.query(User.fullname):
            userlist.append(eachUser)
        print(userlist)
        return userlist
    if listName == 'chapter':
        chapterlist = []
        for eachChapter in session.query(User.chapter):
            chapterlist.append(eachChapter)
        print(chapterlist)
        return chapterlist
    if listName == 'question':
        questionlist = []
        for eachQuestion in session.query(Questions.detail):
            questionlist.append(eachQuestion)
        print(questionlist)
        return questionlist


@app.route('/add_data', methods=['GET','POST'])
def add_data():
    #eventlist = []
    #for eachEvent in session.query(EventInfo.name, EventInfo.year):
    #    eventlist.append(eachEvent)
    #print(eventlist)
    #userlist = []
    #for eachUser in session.query(User.fullname):
    #    userlist.append(eachUser)
    #print(userlist)
    #chapterlist = []
    #for eachChapter in session.query(User.chapter):
    #    chapterlist.append(eachChapter)
    #print(eachChapter)
    eventlist = fetchList(listName='event')
    userlist = fetchList(listName='user')
    chapterlist = fetchList(listName='chapter')
    questionlist = fetchList(listName='question')
    form = SampleLazyForm(request.form)
    if request.method == 'POST':
        lazy = SampleLazy(form.chapterName.data,
                          form.eventName.data,
                          form.shiftLead.data,
                          form.tester.data,
                          form.recorder.data,
                          form.substanceType.data,
            form.substanceDesc.data,
            form.substanceExpe.data,
            form.substanceOther.data,
            form.marquis1.data,
            form.marquis2.data,
            form.marquis3.data,
            form.mecke1.data,
            form.mecke2.data,
            form.mecke3.data,
            form.mandolin1.data,
            form.mandolin2.data,
            form.mandolin3.data,
            form.simon1.data,
            form.simon2.data,
            form.simon3.data,
            form.liebermann1.data,
            form.liebermann2.data,
            form.liebermann3.data,
            form.froehde1.data,
            form.froehde2.data,
            form.froehde3.data,
            form.folin1.data,
            form.folin2.data,
            form.folin3.data,
            form.ehrlich1.data,
            form.ehrlich2.data,
            form.ehrlich3.data,
            form.conclusivebool.data,
            form.conclusiveresult.data,
            form.question1.data,
            form.answer1.data,
            form.question2.data,
            form.answer2.data,
            form.question3.data,
            form.answer3.data,
            form.question4.data,
            form.answer4.data,
            form.question5.data,
            form.answer5.data,
            form.question6.data,
            form.answer6.data,
            form.question7.data,
            form.answer7.data,
            form.question8.data,
            form.answer8.data,
            form.question9.data,
            form.answer9.data,
            form.question10.data,
            form.answer10.data,
            form.question11.data,
            form.answer11.data)

        session.add(lazy)
        session.commit()

        # session.add(
        #         EventInfo(name=eventName,year=eventYear))
        # session.commit()
        # for row in session.query(EventInfo):
        #     print(row)
        print("hey")
        
        chapterName = request.form['chapterName']
        eventName = request.form['eventName']
        shiftLead = request.form['shiftLead']
        tester = request.form['tester']
        recorder = request.form['recorder']
                    
        #session.add(
        #        User(

        # shiftleadName = request.form['shiftleadName']

        # query = "INSERT INTO Testing1(chapterName, eventName, eventYear, shiftleadName) VALUES(%s,%s,%s,%s)"
        # cur.execute(query, (chapterName, eventName, shiftleadName))
        # db.commit()
        # return render_template('survey.html', request.form['eventName'], request.form['eventYear'])
        return redirect(url_for('add_data'))
    return render_template('survey.html', chapterlist=chapterlist, eventlist=eventlist, userlist=userlist, questionlist=questionlist, form=form)

@app.route('/add_event', methods=['GET','POST'])
def add_event():
    form = EventForm(request.form)
    if request.method == 'POST':
        event = EventInfo(form.name.data,
                          form.year.data,
                          form.city.data,
                          form.state.data,
                          form.region.data)
                          #form.datestart.data,
                          #form.dateend.data
        session.add(event)
        session.commit()
        for row in session.query(EventInfo):
            print(row)
        return redirect(url_for('add_event'))
    return render_template('addevent.html', form=form)

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    form = NewUser(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.name.data, form.email.data, form.chapter.data)
        session.add(user)
        session.commit()
        for row in session.query(User):
            print(row)
        flash('Thank you for creating a user!')
        return redirect(url_for('add_user'))
    return render_template('adduser.html', form=form)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    form = NewQuestion(request.form)
    if request.method == 'POST':
        detail = Questions(form.detail.data)
        session.add(question)
        session.commit()
        for row in session.query(Questions):
            print(row)
        return redirect(url_for('add_question'))
    return render_template('addquestion.html', form=form)


app.secret_key = '55823c2e-b31b-4eaf-a44b-025c7fbb1645'

app.run(host='0.0.0.0',port=5001)
