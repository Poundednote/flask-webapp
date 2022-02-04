from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'db1718ede97873dbedc1a95612a1607e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    

gyms = [
    {
        'gym': 'AcademiaBjjLifestyle',
        'instructor': 'Lucio',
        'ranking': '5'
    },
    {
        'gym': 'Stealth BJJ',
        'instructor': 'Steve',
        'ranking': '5'
    }
]
        


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', gyms=gyms)

@app.route('/about')
def about():
    return '<h1>About us</h1>'

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'logged in as {form.email.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)
