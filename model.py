from app import db
from werkzeug.security import generate_password_hash, \
     check_password_hash
from flask_login import UserMixin


class house(db.Model):
	__table__=""
	id = db.column(db.Integer,primary_key= True)