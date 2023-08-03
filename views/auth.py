from time import time
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import request
import smtplib

from . import config
from . import db
from .models import User, Post
from werkzeug.security import generate_password_hash, check_password_hash  #convert password to hash value
from random import randint
from flask_login import login_required, login_user, logout_user, current_user
from flask import session

#import a form class
from .wtforms import *




    
def otp_time():
    Otpstarttime = session["Otpstarttime"]
    Otpendtime = 280
    while True:
        if time() - Otpstarttime >= Otpendtime:
            
            if "passchg_otp" in session:
                session.pop('passchg_otp',None)
                
            else:
                session.pop('Otpstarttime', None)
                session.pop('Otp', None)
                break
        return True

def characters(user_name):
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


def send_mail(email,subject,body):
                
            try:                     
                subject = subject
                body = body
                message = f'Subject:{subject}\n\n{body}'
                server = smtplib.SMTP("smtp.gmail.com",
                                      587)
                server.starttls()
                server.login("config.get()", "config.get()")
                server.sendmail("your Email", email,message)
                
            except smtplib.SMTPException as error:
                flash(f"{error}",
                      category='error')  

auth = Blueprint('auth',
                 __name__,
                 template_folder='../templates',
                 static_folder='../static')





#Loing page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if current_user.is_authenticated :
        flash("Logout your account")
        return redirect(url_for('views.home'))
    else:
        if form.validate_on_submit():
            if request.method == 'POST':
                email = form.email.data
                password = form.password.data

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

    return render_template("login.html",form=form)


#new_password
@auth.route('/new_password', methods=['GET', 'POST'])
def new_password():
    form = NewpasswordForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        
        email=form.email.data
        print(email)
        userEmail = User.query.filter_by(email=email).first()
        if userEmail:
            otp=randint(000000, 999999)  #creat OTP
            session["Otpstarttime"] = time()
            session["passchg_otp"] = otp
            session["email"] = email
            
            subject="OTP"
            body=f"Your OTP:{otp}"
            send_mail(email,subject,body)
            
             
            return redirect(url_for('auth.otp_verfiy'))
        else:
            flash('Email does not exist.', category='error')
            return redirect(url_for('auth.login'))
    return render_template('newPass_email.html',form=form)


@auth.route('/otp_verify', methods=['GET', 'POST'])
def otp_verfiy():
    form=OtpForm()
    if form.validate_on_submit() :
        otp=form.otp.data
        
        print(otp_time())
        if "passchg_otp" in session:
            if  int(otp) == session["passchg_otp"] and otp_time() == True:
                flash('otp macth')
                
                return redirect(url_for('auth.change_password'))
        else:
            flash("OTP Expired", category='error')
            return redirect(url_for('auth.new_password'))
    return render_template('verify.html',form=form)
          

#change password
@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    email=session["email"] 
    user = User.query.filter_by(email=email).first()
    form=NewpasswordForm()
    if form.validate_on_submit() :
        email=form.email.data
        print(email)
        password1=form.password1.data
        password2=form.password2.data

        if len(password1) < 7:
            flash('Passsword must be greater than 6 characters.',
                  category='error')
            return redirect(url_for('auth.change_password'))
        elif password1 != password2:
            flash('password don\'t macth.', category='error')
            return redirect(url_for('auth.change_password'))
        else:
            if password1 == password2 :
                
               
                user.password = generate_password_hash(password1)
                db.session.commit()
                session.pop('passchg_otp',None)
                session.pop('email',None)
                flash("password updated")
                    
                return redirect(url_for('auth.login'))
                
            else:
                return flash(' OTP don\'t macth',category='error')
                
    return render_template('changePassword.html',user=user,form=form)
          
#logout
@auth.route('/logout')
@login_required
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
    form=SingupForm()
   

    return render_template('sign_up.html',form=form)


#verify page, verfiy the email  adderss
@auth.route('/verfiy', methods=['GET', 'POST'])
def verfiy():
    otpForm=OtpForm()  
    form=SingupForm()
    
    if form.validate_on_submit() and request.method == 'POST':
        

        email = form.email.data
        user_name = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data
        gender = form.gender.data
        
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
        elif  characters(user_name) == False :
            flash("must be add Engligh characters", category='error')
            return redirect('/sign-up')
        
        

        else:
            
            otp = randint(000000, 999999)  #creat OTP

            
            Otpstarttime = time()
            session["Otpstarttime"] = Otpstarttime

            session["Otp"] = otp

            session["email"] = email

            session["Name"] = user_name

            session["Password"] = password1
            
            session["gender"] = gender
            print(otp)

            # send otp mail to user mail
            try:
                    
                subject="OTP"
                body=f"Your OTP:{otp}"
                send_mail(email,subject,body)

            except :
                flash("Somthing Error Check Your Email Address",
                      category='error')
            # return redirect('/sign-up')
        return redirect(url_for('auth.verfiy'))
    
    return render_template('verify.html',form=otpForm)




#confirm the OTP
@auth.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if 'Otp' in session:
    
        form= OtpForm()
        print(otp_time())
        if otp_time() == True:

            user_Otp = form.otp.data
            print("User_otp: ",user_Otp)
            
            email = session["email"]
            user_name = session["Name"]
            print("Confirm MAil page=", email)
            password1 = session["Password"]
            gender =session["gender"]

            try:
                int_otp = int(user_Otp)
            except:
                flash('wrong otp!', category='error')
                return render_template('verify.html')

            oTp = session["Otp"]
            if oTp == int_otp:
                
                

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
            flash("OTP Expired", category='error')
            return redirect(url_for('auth.sing_up'))
    else:
        
        return redirect('/login')
    return redirect(url_for('auth.login')) 
