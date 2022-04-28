
from tokenize import Name
from flask import Blueprint, render_template, request,flash,redirect,url_for
from flask import request
import smtplib
from .import db
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from random import randint
from flask_login import login_user,login_required,logout_user,current_user





from matplotlib.pyplot import text
auth = Blueprint('auth', __name__, template_folder='../templates',
                 static_folder='../static')







@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        

        user = User.query.filter_by(email=email).first()
 
        passwordL=check_password_hash(user.password,password)
        print(passwordL)
        if user:
            if passwordL == True:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html",user=current_user)







@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




        

    

    


@auth.route('/sign-up', methods=['GET', 'POST'])
def sing_up():
                        

        return render_template('sign_up.html',user=current_user)
        



                 
@auth.route('/Verify', methods=['GET', 'POST'])
def verfiy(): 
        #get Data from Html
        if request.method == 'POST':
            email = request.form.get('email')            
            user_name = request.form.get('UserName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            print("email:",email)
    

            #checking UserName and Email from Database
            user =User.query.filter_by(email=email).first()
            a=User.query.filter_by(user_name=user_name).first()
    
    

            if  user  :
             flash('Email already exiets', category='error' )
             return render_template('sign_up.html')
             
            elif a:
                print(user_name)
                flash('User Name already exiets', category='error')
                return render_template('sign_up.html')
                
            elif len(email) < 5:
                flash('Email must be greater than 4 characters and check the email address.',category='error')
                return render_template('sign_up.html')
                
            elif len(user_name) > 12:
                flash('User Name must be less than 12 characters.',category='error')
                return render_template('sign_up.html')
                
            elif len(password1) < 7:
                flash('Passsword must be greater than 6 characters.',category='error')
                return render_template('sign_up.html')
                
            elif password1 != password2 :
                flash('password don\'t macth.',category='error')
                return render_template('sign_up.html')
                
                
            else: 
                    otp = randint(000000, 999999)
                    Otp=otp 
                    print("OTP:",Otp) 
                    
                    global OTP 
                    OTP=Otp
                    
                    global EMAIL
                    EMAIL = email
                    
                    global Name
                    Name=user_name
                    
                    global PasswordSing
                    PasswordSing= password1
                    
                    print("Golbal Variable:",EMAIL)
                   
                    # deatils(email,user_name,password1)  
                    try:
                        
                        subject='OTP'
                        body=f'{OTP}'
                        message=f'Subject:{subject}\n\n{body}'
                        print(message)
                        server=smtplib.SMTP("smtp.gmail.com",587)
                        server.starttls()
                        server.login("sabarinathan.project@gmail.com","sabarinathan7")
                        server.sendmail("sabarinathan.project@gmail.com",email,message)

                    except smtplib.SMTPException:
                        flash("Somthing Error Check Your Email Address",category='error') 
                   


            return render_template('verify.html',email=email,user_name=user_name)

@auth.route('/confirm',methods=['GET', 'POST'])
def confirm():  
                        User_Otp=request.form.get('otp')
                        msg='Otp don\'t macth.'

                        email =   EMAIL
                        user_name=Name
                        print("Confirm MAil page=",EMAIL)
                       
                        password1 = PasswordSing
                       
                        
                     
                        int_otp = int(User_Otp)



                        if OTP == int_otp  :

                                    new_user = User(email = email,user_name =user_name,password=(generate_password_hash(password1,MethodType="")))
                                    db.session.add(new_user)
                                    db.session.commit()
                                    flash('Account created!',category='success',)

                                    return redirect(url_for('views.home'))
                        else:
                               
                                
                                return render_template('verify.html',email=email,user_name=user_name,password1=password1,msg=msg)
                        
                        
               
        
            