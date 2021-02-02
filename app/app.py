from flask import flash, render_template, flash, redirect, url_for, request, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/AppDatabase'
app.debug = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniqueID = db.Column(db.String(64), index=True, unique=True)
    Name = db.Column(db.String(64), index=True)
    Message = db.Column(db.String(255))
    Conversation = db.Column(db.String(1000))

    def __init__(self, uniqueID, Name, Message, Conversation):
        self.uniqueID = uniqueID
        self.Name = Name
        self.Message = Message
        self.Conversation = Conversation

    def __repr__(self):
        return '<User {}>'.format(self.uniqueID) 



@app.route('/')
@app.route('/index')
def index():
    return render_template('main-menu.html', title='Home')


@app.route('/sendToDb', methods=['POST'])
def sendToDb():
    error = None
    passMessage = None
    user = User(request.form['Id'], request.form['Name'], request.form['Message'], "")
    db.session.add(user)
    try:
        db.session.commit()
    except:
        error = 'Unique ID already Exists Try again'
        db.session.rollback()
        return render_template('index.html', error=error)
    error = 'Request successfully submitted, please wait and an agent will be with you shortly'
    return render_template('chatroom.html',user=user)
@app.route('/sendChatConversation', methods=['POST'])
def sendChatConversation():
    user_Update = User.query.filter_by(uniqueID="test").first()
    user_Update.Conversation = "This is a test conversation."
    return render_template("index.html",error="sendChatconversation was called, and the table entry was updated.")
@app.route('/customerRender', methods=['GET'])
def customerRender():
    return render_template("index.html")
@app.route('/agentRender', methods=['GET'])
def agentRender():
    rows = User.query.all()
    return render_template("employee-view.html",rows=rows)
@app.route('/MainMenu', methods=['GET'])
def MainMenu():
    return render_template("main-menu.html")   
if __name__ == "__main__":
    app.run()