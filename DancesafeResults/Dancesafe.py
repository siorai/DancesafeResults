from flask import Flask

app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello World!'


""" The following is a proposed list of pages that I want to be accessible to the users of this application
and a brief description of what they will do. 

survey page
    description - survey page, where all the magic happens

add user page
    description - adds a new user to the local database
    
user administration page
    shows various administrative thigns for users like password reset and removal etc
    
add event page 
    allows users with the correct roles to be able to add events to local database

question administration 
    enables configuration of custom pages by the chapterhead to affect the survey page
    should allow the chapter to select new questions, reorder them as they see fit, etc
    
reagent list administration

substance list administration




"""
@app.route('/')
def survey():
    """
    Main page of the survey
    :return:
    """

if __name__ == '__main__':
    app.run()
