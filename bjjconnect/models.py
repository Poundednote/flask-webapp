from bjjconnect import db, login_manager
from flask_login import UserMixin
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    gym_id = db.Column(db.Integer, db.ForeignKey('gym.id'), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', {self.gym.id})'"


class Gym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gym_name = db.Column(db.String(120), unique=True, nullable=False)
    head_instructor = db.Column(db.String(120), unique=True, nullable=False)
    contact_info = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    students = db.relationship('Student', backref='gym')

    def __repr__(self):
        return self.gym_name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Post("{self.title}, "{self.dateposted}")'

