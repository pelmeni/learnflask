from FlaskWebProject1 import db
from FlaskWebProject1 import db_posts
from hashlib import md5

from datetime import datetime
from Crypto import Crypto
import jwt
import os

ROLE_USER = 0
ROLE_ADMIN = 1



class User(db.Model):
    id=db.Column('UserID',db.Integer, primary_key = True)
    username=db.Column('UserName',db.String(50), index = True, unique = True)
    password=db.Column('PasswordHash',db.String(100), index = True, unique = False) 
    email=db.Column('Email',db.String(100), index = True, unique = True)
    registered_on=db.Column('Created' , db.DateTime)
    phone=db.Column('PhoneNumber',db.String(25), index = True, unique = True)
    #Role = db.Column(db.SmallInteger, default = ROLE_USER)

    def __init__(self, username, password, email, phone):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id) # python 2
        except NameError:
            return str(self.id) # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            secret=app.config.get('SECRET_KEY')
            payload = jwt.decode(auth_token, secret)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    
    def hash_password(self, password):
        c=Crypto.CreateWithRfc2898DeriveBytes()
        return c.HashPassword(password)

    def verify_password(self, password):
        c=Crypto.CreateWithRfc2898DeriveBytes()
        return c.VerifyHashedPassword(self.password,password)
    
    def generate_auth_token(self, expiration = 600):
        #s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        #return s.dumps({ 'id': self.id })
        jwt_result=encode_auth_token(self, self.id)
        return jwt;

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)


class Post(db_posts.Model):
    #__bind_key__="posts"
    id = db_posts.Column(db_posts.Integer, primary_key = True)
    body = db_posts.Column(db_posts.String(140))
    timestamp = db_posts.Column(db_posts.DateTime)
    author = db_posts.Column(db_posts.String(50))

    def __repr__(self):
        return '<Post %r>' % (self.body)
   
    def author(self):
        return User.query.filter_by(username = self.author).first()

