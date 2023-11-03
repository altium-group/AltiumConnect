from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import os, datetime

app = Flask(__name__)

app.secret_key = 'defcb16b51fb5722a887a9a904855a57d7eeb584afcaf012'
db_path = os.path.join(os.path.dirname(__file__), 'altium.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    profilePic = db.Column(db.String(120), unique=False, nullable=True)
    creationDate = db.Column(db.String(120), unique=False, nullable=False)

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    Session = sessionmaker(bind=db.engine)
    session_db = Session()
    user = session_db.get(User, session['user_id'])
    session_db.close()
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error=1)
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        if password == confirmpassword:
            userr = User.query.filter_by(username=username).first()
            if not userr:
                user = User(username=username, password=password, creationDate=datetime.datetime.now().timestamp())
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                return render_template('register.html', error=2)
        else:
            return render_template('register.html', error=3)
    
    return render_template('register.html')

@app.route('/profil')
def profil():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('profil.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)