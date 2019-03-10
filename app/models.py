from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin,db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	groups = db.relationship("Group", secondary="user_group", lazy='subquery',backref=db.backref('users', lazy=True))
	posts = db.relationship('Post', backref='author', lazy='dynamic')
	admin = db.relationship('Group',backref='admin', lazy='dynamic')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username) 

class Group(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	des = db.Column(db.String(200))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	invite_code = db.Column(db.String(20))
	posts = db.relationship('Post', backref='group', lazy='dynamic')

	def __repr__(self):
	    return '<Post {}>'.format(self.name)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(500))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
	url = db.Column(db.String(140),default=u'')
	struct = db.Column(db.Integer,default=0)

	def __repr__(self):
		return '<Post {}>'.format(self.body)

user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))