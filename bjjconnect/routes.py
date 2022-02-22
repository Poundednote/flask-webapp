from flask import render_template, url_for, flash, redirect, session
from bjjconnect.forms import  RegistrationForm, LoginForm, GymRegistrationForm, UserForm
from bjjconnect.models import Student, Gym
from bjjconnect import app, db, bcrypt
from flask_login import login_user, current_user

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
    if current_user.is_authenticated:
        return current_user.password

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        # generates hashed password and stores gym in database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Student(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/gym_register', methods=['GET', 'POST'])
def gym_register():
    form = GymRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Gym(gym_name=form.gym_name.data, email=form.email.data, contact_info=form.phone_contact.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Gym created under name {form.gym_name.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('gymregistration.html', title='Gym Register', form=form)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.email.data).first()  # finds matching user in db
        if user and bcrypt.check_password_hash(user.password, form.password.data): # checks if user exists and password matches users
            login_user(user, remember=form.remember.data)  # flask login modules handles user login and session data
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = UserForm()
    if current_user.is_authenticated:
        return render_template('user.html', title=current_user.username, user=current_user, form=form)
    else:
        return redirect(url_for('login'))

    if form.validate_on_submit():
        user = current_user.get_current_object()
        if bcrypt.check_password_hash(user.password, form.password.data):
            if form.username.data:
                user.username = form.username.data
            if form.email.data:
                user.email = form.username.data

                db.session.commit()

            return render_template('user.html', title=current_user.username, user=current_user, form=form)

