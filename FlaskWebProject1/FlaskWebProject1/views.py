
from datetime import datetime
from flask import render_template, flash, redirect,session, url_for,request, g,redirect
from flask_login import login_user, logout_user, current_user, login_required
from FlaskWebProject1 import app, db, lm
from .forms import LoginForm
from .models import User, ROLE_USER, ROLE_ADMIN


@app.route('/api/token')
@login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/hello')
@login_required
def hello():
     user = g.user;
     posts = [ # список выдуманных постов
        { 
            'author': { 'nickname': 'John' }, 
            'body': 'Beautiful day in Portland!!!' 
        },
        { 
            'author': { 'nickname': 'Susan' }, 
            'body': 'The Avengers movie was so cool!!!' 
        }
     ]
     return render_template('hello.html', user=user, posts=posts)

@app.route('/login', methods = ['POST'])
def login():
       
    post_data = request.get_json()

    username=request.form.get('username')
    password=request.form.get('password')

    remember_me = False
   
    session['remember_me']= 'remember_me' in request.form
                 
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'));

    if not user.verify_password(password):
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'));
        
    flash('Logged in successfully')
    
    login_user(user, remember = session['remember_me'])

    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('hello'))

    return redirect(request.args.get('next') or url_for('home'))

@app.route('/login', methods = ['GET'])
def login_get():

    form = LoginForm()

    return render_template('login.html', title = 'Sign In', form = form)
    

@app.before_request
def before_request():
    g.user=current_user

#def after_login(resp):
#    if resp.email is None or resp.email == "":
#        flash('Invalid login. Please try again.')
#        return redirect(url_for('login'))
#    user = User.query.filter_by(email = resp.email).first()
#    if user is None:
#        nickname = resp.nickname
#        if nickname is None or nickname == "":
#            nickname = resp.email.split('@')[0]
#        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
#        db.session.add(user)
#        db.session.commit()
 

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('hello')) 


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(username = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('hello'))
    posts = [
        { 'author': user, 'body': 'Test post #1' },
        { 'author': user, 'body': 'Test post #2' }
    ]
    return render_template('user.html', user = user, posts = posts)
