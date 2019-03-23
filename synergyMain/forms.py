from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, IntegerField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, NumberRange, ValidationError
from synergyMain.models import User, Conversing, Conversation

class SelectForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(max=120) ,Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_name = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    user_interests = [('M','Machine Learning'),('B', 'Blockchain'),('C', 'Cybersecurity')]
    user_interests = [('0','Machine Learning'),('1', 'Blockchain'),('2', 'Cybersecurity')]
    user_interest1 = SelectField('Interest', choices=user_interests, validators=[Required()])
    user_interest2 = SelectField('Interest', choices=user_interests, validators=[Required()])
    user_about =  TextAreaField('About Your Organization', validators=[DataRequired()] )
    user_logo = FileField('Logo',validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Proceed')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Tha email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')




class UpdateAccountForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(max=120) ,Email()])
    password = PasswordField('Update Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_name = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
<<<<<<< HEAD
    user_interests = [('M','Machine Learning'),('B', 'Blockchain'),('C', 'Cybersecurity')]
=======
    user_interests = [('0','Machine Learning'),('1', 'Blockchain'),('2', 'Cybersecurity')]
>>>>>>> 85c44d0f8679554377b14704cb2587260a003967
    user_interest1 = SelectField('Your area of Interest', choices=user_interests, validators=[Required()])
    user_interest2 = SelectField('Your area of Interest', choices=user_interests, validators=[Required()])
    user_about =  TextAreaField('About Your Organization', validators=[DataRequired()] )
    user_logo = FileField('Update your Profile Picture',validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Proceed')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Tha email is taken. Please choose a different one.')




class ChatBoxText(FlaskForm):
    text = StringField('Enter Text', validators=[DataRequired(), Length(min=1, max=500)])
    send = SubmitField('Send')


class RequestForm(FlaskForm):
    invite_status = RadioField('You have an invite!', choices=[('1','Accept'),('0','Decline')])
    submit=SubmitField('Submit')

class InviteForm(FlaskForm):
    invite = SubmitField('Invite')
