from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    username=TextField('username', validators = [Required()])
    password=TextField('password', validators = [Required()])
    #openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


