from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FieldList, SelectField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from bjjconnect import bcrypt
from bjjconnect.models import Student, Gym

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    gym = QuerySelectField(query_factory=lambda:Gym.query, allow_blank=True)
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Student.query.filter_by(username=username.data).all()
        print(user)

        if user: 
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).all()

        if user: 
            raise ValidationError('Email already in use')




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class GymRegistrationForm(FlaskForm):
    gym_name = StringField('Gym name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    head_instructor = StringField('Head Instructor', validators=[DataRequired()])

    other_instructors = FieldList(StringField('Other Instructors', validators=[Length(max=50)]), max_entries=4),

    phone_contact = StringField('Phone Contact')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Gym')
    
class UserForm(FlaskForm):
    username = StringField('Username', validators=[Optional(), Length(min=3, max=30)])
    email = StringField('Email', validators=[Optional(), Email()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=400)])
    password = PasswordField('Password', validators=[DataRequired()])
    belt = SelectField('Belt', choices=[('w','White'), ('bl', 'Blue'), ('p','Purple'), ('brn','Brown'), ('blk','Black')])
    submit = SubmitField('Apply')
    gym = QuerySelectField(query_factory=lambda:Gym.query, allow_blank=True)

    def validate_username(self, username):
        user = Student.query.filter_by(username=username.data).all()

        if user:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        email = Student.query.filter_by(email=email.data).all()

        if email:
            raise ValidationError('Email already in use')

class PostForm:
    title = StringField('Title', validators=[Length(max=120), DataRequired()])
    content = TextAreaField('Content', validators=[Length(max=120), DataRequired()])
    submit_post = SubmitField('Post')

