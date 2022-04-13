from unicodedata import name
from flask import Blueprint, render_template, request,flash
from flask import request
import os 


from matplotlib.pyplot import text
auth = Blueprint('auth', __name__, template_folder='../templates',
                 static_folder='../static')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return render_template('logout.html')


@auth.route('/sing-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        email = request.form.get('email')
        UserName = request.form.get('UserName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(email) < 5:
            
            flash('Email must be greater than 4 characters and check the email address.',category='error')
        elif len(UserName) > 12:
             flash('Name must be less than 12 characters.',category='error')
        elif len(password1) < 8:
             flash('Passsword must be greater than 8 characters.',category='error')
        elif password1 != password2 :
            flash('password don\'t macth.',category='error')
        else:
            #add user to database
            flash('Account created!',category='success')
        



    return render_template('sign_up.html')
