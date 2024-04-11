from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Note(db.Model, UserMixin):
    __tablename__ = 'note'  
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    age = db.Column(db.Integer) 

    bmi_entries = relationship("BMIEntry", back_populates="user")

    def __init__(self, email, password, first_name, age=None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.age = age

class BMIEntry(db.Model, UserMixin):
    __tablename__ = 'bmi_entry'
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    bmi = db.Column(db.Float)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10), nullable=False)
    family_history = db.Column(db.String(3), nullable=False)
    favc = db.Column(db.String(3), nullable=False)
    fcvc = db.Column(db.Integer, nullable=False)
    ncp = db.Column(db.Integer, nullable=False)
    caec = db.Column(db.String(10), nullable=False)
    smoke = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="bmi_entries")

    def __init__(self, weight, height, bmi, age, gender, family_history, favc, fcvc, ncp, caec, smoke, user_id):
        self.weight = weight
        self.height = height
        self.bmi = bmi
        self.age = age
        self.gender = gender
        self.family_history = family_history
        self.favc = favc
        self.fcvc = fcvc
        self.ncp = ncp
        self.caec = caec
        self.smoke = smoke
        self.user_id = user_id
