
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Users(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),nullable=False,unique=True)
    password=db.Column(db.String(128)) 

    def __init__(self, username,password):
      self.username = username
      self.password = password


class Students(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text)
    address=db.Column(db.Text)
    city=db.Column(db.Text)
    pin=db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.name}>'

    def __init__(self, name, address, city, pin):
      self.name = name
      self.address = address
      self.city = city
      self.pin = pin