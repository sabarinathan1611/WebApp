from flask import Blueprint,render_template,request
from flask_login import login_required,current_user
from .models import User, Note


views= Blueprint('views',__name__, template_folder='../templates', static_folder='../static')

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    user=current_user
    name=user.user_name
    
    
    
    return render_template('home.html',user=user,name=name)

