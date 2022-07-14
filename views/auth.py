from crypt import methods
import re
from time import time
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import request
import smtplib

from matplotlib.backend_bases import RendererBase  #for mail sending
from . import db
from .models import User, Image
from werkzeug.security import generate_password_hash, check_password_hash  #convert password to hash value
from random import randint
from flask_login import login_user, logout_user, current_user
from flask import session
from datetime import timedelta
from . import create_app
    
def otp_time():
    Otpstarttime = session["Otpstarttime"]
    Otpendtime = 180
    while True:
        if time() - Otpstarttime >= Otpendtime:
            flash("OTP Expired", category='error')
            session.pop('Otpstarttime', None)
            session.pop('Otp', None)
            break
        return True

def Name(user_name):
    num=65
    A=chr(num)
    name=user_name
    while True:
            
            letter=chr(num)
            lower=letter.lower()
            

            if letter in  name or lower in name:
                return True
                
            num=num+1
            if num == 91:
                break
    return bool()

def OTP(Otp,email):
                
            try: 
                subject = 'OTP'
                body = f'otp:{Otp}'
                message = f'Subject:{subject}\n\n{body}'
                print(message)
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login("sabarinathan.project@gmail.com", "#sabarinathan7812885388")
                server.sendmail("sabarinathan.project@gmail.com", email,
                                message)
            except smtplib.SMTPException:
                flash("Somthing Error Check Your Email Address",
                      category='error')  

auth = Blueprint('auth',
                 __name__,
                 template_folder='../templates',
                 static_folder='../static')

#Loing page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated :
        flash("Logout your account")
        return redirect('/')
    else:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password1')

            user = User.query.filter_by(email=email).first()  #check email from db

            if user:
                if check_password_hash(user.password,
                                    password):  #check the password from db
                    flash('Logged in successfully!', category='success')
                    login_user(user,remember=False)

                   
                    session["user_id"] = user.id

                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')

    return render_template("login.html")


#new_password
@auth.route('/new_password', methods=['GET', 'POST'])
def new_password():
    if request.method =='POST':
        email=request.form.get('email')
        userEmail = User.query.filter_by(email=email).first()
        if userEmail:
            Otp=randint(000000, 999999)  #creat OTP
            Otpstarttime = time()
            session["Otpstarttime"] = Otpstarttime
            session["Otp"] = Otp
            session["email"] = email
            OTP(Otp,email)
             
            return redirect(url_for('auth.change_password'))
        else:
            flash('Email does not exist.', category='error')
            return redirect(url_for('auth.login'))
    return render_template('newPass_email.html')

#change password
@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    email=session["email"] 
    user = User.query.filter_by(email=email).first()
    if otp_time() == True:
        if request.method =='POST':
            password1=request.form.get('password1')
            password2=request.form.get('password2')
            
            if password1 == password2:
                user.password = generate_password_hash(password1)
                db.session.commit()
                flash("password updated")
                return redirect('/login')
            else:
                flash('password don\'t macth.', category='error')
                
    return render_template('changePassword.html',user=user)
          
#logout
@auth.route('/logout')
def logout():
    if "user_id" in session:
        if  f"admin_login{current_user.id}" in session :       
            session.pop(f"admin_login{current_user.id}", None)
        logout_user()
        session.pop("user_id", None)
        return redirect(url_for('auth.login'))
    else:

        return redirect(url_for('auth.login'))

#Sing up page
@auth.route('/sign-up', methods=['GET', 'POST'])
def sing_up():
    return render_template('sign_up.html')


#verify page, verfiy the email  adderss
@auth.route('/Verify', methods=['GET', 'POST'])
def verfiy():

    #get Data from Html
    if request.method == 'POST':
        

        email = request.form.get('email')
        user_name = request.form.get('UserName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        gender = request.form.get('gender')
        print("email:", gender)

        #checking UserName and Email from Database
        user = User.query.filter_by(email=email).first()
        userName = User.query.filter_by(user_name=user_name).first()

        if user:
            flash('Email already exiets', category='error')
            return redirect('/sign-up')

        elif userName:
            print(user_name)
            flash('User Name already exiets', category='error')
            return redirect('/sign-up')

        elif len(email) < 5:
            flash(
                'Email must be greater than 4 characters and check the email address.',
                category='error')
            return redirect('/sign-up')

        elif len(user_name) > 12 and len(user_name) < 1:
            flash(
                'User Name must be less than 12 characters and greater than 1 characters.',
                category='error')
            return redirect('/sign-up')

        elif len(password1) < 7:
            flash('Passsword must be greater than 6 characters.',
                  category='error')
            return redirect('/sign-up')

        elif password1 != password2:
            flash('password don\'t macth.', category='error')
            return redirect('/sign-up')
        elif gender == None:
            flash(
                'Select Your Gender',
                category='error')

            return redirect('/sign-up')
        elif  Name(user_name) == False :
            flash("must be add letter", category='error')
            return redirect('/sign-up')
        
        

        else:
            
            otp = randint(000000, 999999)  #creat OTP

            Otp = otp
            Otpstarttime = time()
            session["Otpstarttime"] = Otpstarttime

            session["Otp"] = Otp

            session["email"] = email

            session["Name"] = user_name

            session["Password"] = password1
            
            session["gender"] = gender
            

            # send otp mail to user mail
            try:

               OTP(Otp,email)

            except smtplib.SMTPException:
                flash("Somthing Error Check Your Email Address",
                      category='error')
            # return redirect('/sign-up')
    else:
        return redirect('/login')

    return render_template('verify.html')




#confirm the OTP
@auth.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if 'Otpstarttime' in session:
    
        
        if otp_time() == True:

            User_Otp = request.form.get('otp')

            email = session["email"]
            user_name = session["Name"]
            print("Confirm MAil page=", email)
            password1 = session["Password"]
            gender =session["gender"]

            try:
                int_otp = int(User_Otp)
            except:
                flash('wrong otp!', category='error')
                return render_template('verify.html')

            OTp = session["Otp"]
            if OTp == int_otp:
                
                

                new_user = User(email=email,
                                user_name=user_name,
                                gender =gender,
                                # admin= True,
                                password=(generate_password_hash(password1)))
                db.session.add(new_user)
                db.session.commit()

                
                session.pop("Password", None)
                session.pop('email',None)
                session.pop('Name',None)
                session.pop("gender", None)

                flash('Account created!', category='success')

                return redirect(url_for('views.home'))
            else:
                flash('wrong otp!', category='error')
        else:
            return redirect(url_for('auth.sing_up'))
    else:
        return redirect('/login')
    return redirect(url_for('auth.login'))
