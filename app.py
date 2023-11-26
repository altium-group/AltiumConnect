from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from sqlalchemy.orm import sessionmaker
import os, datetime, base64, hashlib
from flask_migrate import Migrate
from PIL import Image
from io import BytesIO
from sqlalchemy import create_engine

app = Flask(__name__)

@app.template_filter('b64decode')
def base64decode(value):
    return base64.b64decode(value)

app.jinja_env.filters['b64decode'] = base64.b64decode

app.secret_key = 'defcb16b51fb5722a887a9a904855a57d7eeb584afcaf012'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\noanh\\OneDrive\\Documents\\AltiumConnect\\altium.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    profilePic = db.Column(LargeBinary, nullable=True)
    birth = db.Column(db.String(120), unique=False, nullable=True)
    phone = db.Column(db.String(120), unique=False, nullable=True)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    identity = db.Column(db.String(120), unique=False, nullable=True)
    language = db.Column(db.String(120), unique=False, nullable=True)
    nationality = db.Column(db.String(120), unique=False, nullable=True)
    status = db.Column(db.String(120), unique=False, nullable=True)
    lastConnexion = db.Column(db.String(120), unique=False, nullable=True)
    creationDate = db.Column(db.String(120), unique=False, nullable=False)

with app.app_context():
    db.create_all()

def hash_string(input_string):
    sha256 = hashlib.sha256()
    input_bytes = input_string.encode('utf-8')
    sha256.update(input_bytes)
    hashed_string = sha256.hexdigest()
    return hashed_string

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=hash_string(password)).first()
        if user:
            session['user_id'] = user.id
            user.lastConnexion = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            db.session.commit()
            return redirect(url_for('home'))
        else:
            return render_template('login.html', code=1)
    
    return render_template('login.html')

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    Session2 = sessionmaker(bind=db.engine)
    session_db = Session2()
    user = session_db.get(User, session['user_id'])
    session_db.close()
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        if password == confirmpassword:
            userr = User.query.filter_by(username=username).first()
            if not userr:
                user = User(username=username, password=hash_string(password), status="user", lastConnexion=datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'), creationDate=datetime.datetime.now().timestamp())
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                return render_template('register.html', code=2)
        else:
            return render_template('register.html', code=3)
    
    return render_template('register.html')

@app.route('/profil', methods=['GET', 'POST'])
def profil():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    Session2 = sessionmaker(bind=db.engine)
    session_db = Session2()
    user = session_db.get(User, session['user_id'])

    if request.method == 'POST':
        password = request.form['password']
        if password == user.password:
            for key in request.form:  
                values = request.form.getlist(key)
                if key == "password":
                    continue
                setattr(user, key, values[0])
            session_db.commit()
            session_db.close()
            return redirect(url_for('profil'))
        else:
            return render_template('profil.html', code=6, user=user)
    else:
        return render_template('profil.html', user=user)

@app.route('/adminpanel')
def adminpanel():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    Session2 = sessionmaker(bind=db.engine)
    session_db = Session2()
    user = session_db.get(User, session['user_id'])
    session_db.close()
    if user.status == "admin":
        return render_template('adminpanel.html', user=user)
    else:
        return redirect(url_for('home'))

@app.route('/adminpanel/userlist')
def userlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    Session2 = sessionmaker(bind=db.engine)
    session_db = Session2()
    user = session_db.get(User, session['user_id'])
    session_db.close()
    
    if user.status == "admin":
        engine = create_engine('sqlite:///C:\\Users\\noanh\\OneDrive\\Documents\\AltiumConnect\\altium.db')
        Session2 = sessionmaker(bind=engine)
        sqlalchemy_session = Session2()

        results = sqlalchemy_session.query(User).all()

        sqlalchemy_session.close()

        return render_template('userlist.html', user=user, userlist=results)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)