from app import app,db
from flask import render_template, redirect, url_for, request,flash
from app.models import User,Post,Group
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from random import randint
import time
from werkzeug import secure_filename
import os
from sqlalchemy import or_

@app.route('/')
@app.route('/index/')
def index():
	if current_user.is_authenticated:
		return redirect(url_for('dashboard'))
	return render_template('landing.html')

@app.route('/getstarted/')
def start():
	if current_user.is_authenticated:
			return redirect(url_for('dashboard'))
	return render_template('loginrg.html',reg=0)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method=="GET":
		if current_user.is_authenticated:
			return redirect(url_for('dashboard'))
		return render_template('loginrg.html')
	else:
		user = User.query.filter_by(username=request.form['name']).first()
		if user is None or not user.check_password(request.form['password']):
			return redirect(url_for('login'))
		login_user(user)
		next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)

@app.route('/register/', methods=['POST','GET'])
def register():	
	if request.method=='GET':
		return render_template('loginrg.html')
	else :
		u = User.query.filter(or_(User.username==request.form['uname'],User.email==request.form['email'])).first()
		if u is None:
			u = User(name=request.form['name'],username=request.form['uname'],email=request.form['email'])
			u.set_password(request.form['password'])
			db.session.add(u)
			db.session.commit()
			return render_template('loginrg.html',reg=1)
		else:
			return render_template('loginrg.html',reg=-1)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard/')
@login_required
def dashboard():
	return render_template('dashboard.html',current_user=current_user)

@app.route('/create', methods = ['POST','GET'])
@login_required
def create():
	if request.method=='GET':
		return render_template('create.html')
	else:
		g = Group(name=request.form['name'],des=request.form['des'],invite_code=randint(100000,999999),admin=current_user)
		db.session.add(g)
		db.session.commit()
		return redirect(url_for('groupView',id=g.id))

@app.route('/join', methods = ['POST','GET'])
@login_required
def join():
	if request.method=='GET':
		return render_template('join.html')
	else:
		g = Group.query.filter_by(id=request.form['id']).first()
		if g is None or not g.invite_code==request.form['invite_code']:
			return "ERROR Check Grp Id and Invite Code"
		g.users.append(current_user)
		db.session.commit()
		return redirect(url_for('groupView',id=g.id))

@app.route('/group/<id>')
@login_required
def groupView(id):
	g = Group.query.filter_by(id=id).first();
	if g is None:
		return redirect(url_for('index'))
	posts = Post.query.filter_by(group_id=g.id)
	if g.admin_id==current_user.id:
		return render_template('groupview.html',g=g,post=posts)
	q = current_user.groups
	for i in q:
		if i.id==g.id:
			return render_template('groupview.html',g=g,post=posts)
	return render_template('dashboard.html',f=1)

@app.route('/post', methods=['POST'])
@login_required
def post():
	exts = ['jpg','jpeg','png','gif']
	try:
		if request.files['file'].filename == '':
			p = Post(body=request.form['body'])
		else:
			s=0
			f =request.files['file']
			name = str(time.time())+str(current_user.id)+f.filename
			f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(name)))
			ext = name.split('.')[-1]
			if ext in exts:
				s=1
			p = Post(body=request.form['body'],url=name,struct=s)
	except Exception as e:
		print(e)
		p = Post(body=request.form['body'])
	g = Group.query.filter_by(id=request.form['id']).first()
	g.posts.append(p)
	current_user.posts.append(p)
	db.session.add(p)
	db.session.commit()
	return	redirect(url_for('groupView',id=g.id))

@app.route('/uploads/<path:path>')
def send_js(path):
    return send_from_directory('uploads', path)

