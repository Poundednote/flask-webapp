from flask import render_template, url_for, flash, redirect, session, request, make_response
from bjjconnect.forms import  RegistrationForm, LoginForm, GymRegistrationForm, UserForm
from bjjconnect.models import Student, Gym, Post
from bjjconnect import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
    user = current_user
    posts = Post.query.all()
    return render_template('home.html', gyms=gyms, posts=posts, user=user)

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
        # generates hashed password and stores user in database
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Student(username=form.username.data, email=form.email.data, password=hashed_password, gym=form.gym.data)
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    form = UserForm()

    if form.validate_on_submit():
        user = current_user
        if bcrypt.check_password_hash(user.password, form.password.data):
            if form.username.data:
                user.email = form.username.data 

            if form.email.data:
                user.email = form.username.data

            if form.gym.data:
                user.gym = form.gym.data

            db.session.commit()

            flash(f'Changes Successful', 'success')

        else:
            flash(f'Changes Unsuccessful. Please check password', 'success')
        
    return render_template('user.html', title=current_user.username, user=current_user, form=form)
        
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.errorhandler(404)
def not_found(e):
    return make_response(render_template("404.html"), 404)
