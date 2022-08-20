from distutils.text_file import TextFile
from email.policy import default
from tokenize import String
from django.forms import IntegerField
from flask_login import current_user
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import EmailField,StringField,PasswordField,SubmitField,SelectField,IntegerField,TextAreaField
from wtforms.validators import *
from flask_wtf.file import FileField



class SingupForm(FlaskForm):
    email = EmailField("Email",validators=[InputRequired()])
    username = StringField("Username",validators=[DataRequired("Username Required"),length(min=4,max=12,message="Must be between 5 charactres")])
    password1 = PasswordField("Password",validators=[DataRequired(),length(min=8,message="Passsword must be greater than 8 characters.")])
    password2 = PasswordField("Password(confirm)",validators=[DataRequired(),length(min=8,message="Passsword must be greater than 8 characters.")])
    gender = SelectField('gender', choices = [('Female', 'Female'), 
      ('Male', 'Male'),('Other','Other')])
    submit=SubmitField("Submit")
    
    
class OtpForm(FlaskForm):
    otp = IntegerField("otp",validators=[InputRequired()])
    
    submit=SubmitField("Submit")
    
class NewpasswordForm(FlaskForm):
    email=EmailField("Email",validators=[InputRequired()])
    password1 = PasswordField("Password")
    password2 = PasswordField("Password(confirm)")
    submit=SubmitField("Submit")
    
    
    
class LoginForm(FlaskForm):
    email = EmailField("Email",validators=[InputRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    recaptcha=RecaptchaField()
    submit=SubmitField("Login")
    
    
class Createpost(FlaskForm):
    
    content=TextAreaField("content",validators=[DataRequired()])
    
    submit=SubmitField("Post")
    

class ImageForm(FlaskForm):
    
    content   = StringField("caption",validators=[DataRequired("caption Required"),length(min=4,max=50,message="Must be between 5 and 50 charactres")])
    submit    = SubmitField("PostImage")
    
    
    
class Profileupdate(FlaskForm):
    fullname  = StringField("Full Name",validators=[DataRequired("Name Required"),length(min=4,max=20,message="Must be between 5 and 20 charactres")])
    bio       = StringField("Bio",validators=[InputRequired()])
    image     = FileField('image')
    submit    = SubmitField("Updat Profile")
    
class Editadmin(FlaskForm):
    email     = EmailField("Email",validators=[InputRequired()])
    password1  = PasswordField("Password")
    password2 = PasswordField("Password(confirm)")
    fullname  = StringField("Full Name",validators=[DataRequired("Name Required"),length(min=4,max=20,message="Must be between 5 and 20 charactres")])
    submit    = SubmitField("Updat Profile")
    
class Useredit(FlaskForm):
    username = StringField("Username",validators=[DataRequired("Username Required"),length(min=4,max=12,message="Must be between 5 charactres")])
    email     = EmailField("Email",validators=[InputRequired()])
    fullname  = StringField("Full Name",validators=[DataRequired("Name Required"),length(min=4,max=20,message="Must be between 5 and 20 charactres")])
    bio       = StringField("Bio",validators=[InputRequired()])
    gender = SelectField('gender', choices = [('Female', 'Female'), ('Male', 'Male'),('Other','Other')])
    submit=SubmitField("Submit")
    fullname  = StringField("Full Name",validators=[DataRequired("Name Required"),length(min=4,max=20,message="Must be between 5 and 20 charactres")])
    submit    = SubmitField("Updat Profile")
    
class SearchForm(FlaskForm):
    search = StringField("Serach",validators=[InputRequired()])
    submit    = SubmitField("Search")