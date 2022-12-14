from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

#Create change number form class
class ChangeNumberForm(FlaskForm):
    number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

#Create login form class
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

#Create transfer form class
class TransferForm(FlaskForm):
    to_account = StringField('To Account', validators=[DataRequired()])
    from_account = StringField('From Account', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Submit')