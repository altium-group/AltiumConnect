from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from sqlalchemy.orm import sessionmaker
import os, datetime, base64
from flask_migrate import Migrate

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
            user.lastConnexion = datetime.datetime.now().timestamp()
            db.session.commit()
            db.session.close()
            return redirect(url_for('home'))
        else:
            return render_template('login.html', code=1)
    
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
                user = User(username=username, password=password, lastConnexion=datetime.datetime.now().timestamp(), creationDate=datetime.datetime.now().timestamp())
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
    
    Session = sessionmaker(bind=db.engine)
    session_db = Session()
    user = session_db.get(User, session['user_id'])

    if request.method == 'POST':
        password = request.form['password']
        if password == user.password:
            if 'profilePic' in request.files:
                profile_pic = request.files['profilePic']
                if profile_pic:
                    image_data = profile_pic.read()
                    user.profilePic = base64.b64encode(image_data)
            for key in request.form:  
                values = request.form.getlist(key)
                if key == "password":
                    continue
                setattr(user, key, values[0])
            session_db.commit()
            session_db.close()
            return redirect(url_for('profil'))
        else:
            return render_template('profil.html', code=6)
    else:
        return render_template('profil.html', user=user)

@app.route('/adminpanel')
def adminpanel():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    Session = sessionmaker(bind=db.engine)
    session_db = Session()
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
    
    Session = sessionmaker(bind=db.engine)
    session_db = Session()
    user = session_db.get(User, session['user_id'])
    session_db.close()
    if user.status == "admin":
        return render_template('adminpanel.html', user=user)
    else:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)