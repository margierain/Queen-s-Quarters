# import db
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_login import UserMixin
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', backref='role')



class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(128))
    # roles = db.relationship(
    #     'Role',
    #     secondary='roles',
    #     backref=db.backref('users', lazy='dynamic')
    # )
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


    @property
    def password(self):
        raise AttributeError(' incorrect password ')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def __init__(self,name, email, password):
    #     self.name = name
    #     self.email = email
    #     self.password = password


class Role1(db.Model):
    __tablename__ = 'role1'
    id = db.Column(db.Integer, primary_key=True)
    queens = db.relationship('House', backref='role1')#) lazy='immediate')



class House(UserMixin, db.Model):
    __tablename__="queens"
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(255), unique = True)
    houseType = db.Column(db.String(255))
    location =db.Column(db.String(255))
    bedrooms = db.Column(db.Integer)
    price = db.Column(db.Integer)
    images = db.Column(db.String(255))
    role1_id = db.Column(db.Integer, db.ForeignKey('role1.id'))
    
    # roles1 = db.relationship('Role1',
    #     secondary= 'role1',
    #     backref =db.backref('queens', lazy='immediate')
    #     )
   

    def __repr__(self):
        return '<{}-{}--{}-{} >'.format(self.name, self.houseType, self.bedrooms, self.price)

if __name__ == '__main__':
    db.create_all()


# class Role(db.Model):
# # ...
# users = db.relationship('User', backref='role')
# class User(db.Model):
# # ...



