from flask import Flask, render_template, request
import MySQLdb


app = Flask(__name__)

db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="dancesafedancesafe",
        db="DS_Testing"
        )

cur = db.cursor()



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/add_data', methods=['GET','POST'])
def add_data():
    if request.method == 'POST':
        chapterName = request.form['chapterName']
        eventName = request.form['eventName']
        eventYear = request.form['eventYear']
        shiftleadName = request.form['shiftleadName']

        query = "INSERT INTO Testing1(chapterName, eventName, eventYear, shiftleadName) VALUES(%s,%s,%s,%s)"
        cur.execute(query, (chapterName, eventName, shiftleadName))
        db.commit()
        return 'Submitted...?'
    return render_template('survey.html')

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    add_data()
    return render_template('survey.html')
