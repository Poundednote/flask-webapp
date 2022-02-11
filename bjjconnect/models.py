from bjjconnect import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    gym = db.Column(db.Integer, db.ForeignKey('gym.id'))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', {self.image_file})'"


class Gym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gym_name = db.Column(db.String(120), unique=True, nullable=False)
    head_instructor = db.Column(db.String(120), unique=True, nullable=False)
    contact_info = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    students = db.relationship('Student', backref='Gym')

    def __repr__(self):
        return f"Gym('{self.gym_name}', '{self.head_instructor}', {self.contact_info}'"
