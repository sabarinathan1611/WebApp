from datetime import timedelta
import json
import os
from random import randint
import uuid
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask import session
from .models import  Post, User, Admin,Comment,Post_like
from . import db
from . import create_app
from werkzeug.utils import secure_filename  #for secure file

from.wtforms import *
from werkzeug.security import generate_password_hash,check_password_hash
views = Blueprint('views',
                  __name__,
                  template_folder='../templates',
                  static_folder='../static')

app = create_app()

# runs before FIRST request (only once)

@app.before_first_request  
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=3)
    


#Allowed Extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp','raw','svg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit(
        '.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Main page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if "user_id" in session:
        if session["user_id"] == current_user.id:
            user = current_user
            session["user_name"] = user.user_name
            posts = Post.query.order_by(Post.date)
            
        else:
            return redirect(url_for('auth.singup'))


            
    else:
        return redirect(url_for('auth.login'))

    return render_template('home.html',posts=posts)


#My post
@views.route('/my-post', methods=['GET', 'POST'])
@login_required
def my_post():
    

    user=User.query.get_or_404(current_user.id)
    return render_template('my_post.html', posts=user.posts)



#Createposts
@views.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    
    form= Createpost()
    if request.method == 'POST':

                pic = request.files['image']
                post = request.form.get('post')
                print("PIc:",len(pic.filename))
                print("post",post)

                if len(pic.filename) < 1 and  len(post) < 1 :
                    flash('Error')
                    return redirect('/')
                
                
                else:
                    if len(pic.filename) > 1:
                        if  allowed_file(pic.filename) == False:
                            flash("Allowed file 'png', 'jpg', 'jpeg', 'webp','raw','svg'")
                        else:
                            print(allowed_file(pic.filename))

                            filename = secure_filename(pic.filename)

                            random_num = str(randint(0000000000, 9999999999))

                            pic_name = str(uuid.uuid1()) + "_" + random_num + "_" + filename
                            print("filename:", pic_name)

                            pic.save(os.path.join(app.config['POST_FOLDER'], pic_name))

                            mimetype = pic.mimetype
                            new_post = Post(post=post, user_id=current_user.id,img_name=pic_name,mimetype=mimetype)
                            db.session.add(new_post)
                            db.session.commit()
                            flash('POST created!', category='success')
                        return redirect('/')
                    elif len(post) > 1 :
                        new_post = Post(post=post, user_id=current_user.id,)
                        db.session.add(new_post)
                        db.session.commit()
                        flash('POST created!', category='success')
                    return redirect('/')
    return render_template('creat_post.html',form=form)


# editpage
@views.route('/edit-note/<int:id>', methods=['POST','GET'])
@login_required
def edit_note(id):
    form = Createpost()
    post = Post.query.get(id)
    form.post.data=post.post
    
    if current_user.id == post.user_id or current_user.admin == True:   
        
        return render_template('editpost.html',post=post,form=form)
    
    else:
        flash("you can't Edit other user post",category='error')
        return redirect(url_for('views.home'))

#Update post
@views.route('/update-note/<int:id>', methods=['POST','GET'])
@login_required
def update_note(id):
    post = Post.query.get(id)
    if current_user.id == post.user_id or current_user.admin == True:    
        
        if request.method == 'POST':
            new_post = request.form.get('post')
            print(new_post)
            if len(new_post) < 1 :
                flash('Note is too short!', category='error')
                return redirect(url_for('views.edit_note',id=post.id))
            else:
                print("yessss")
                Post.query.filter_by(id=post.id).update(dict(post=new_post,edited=True))
                db.session.commit()
                flash('NOTE update!', category='success')
    return redirect('/')
            
#comment post 
@views.route("/comment/<post_id>",methods=['POST','GET'])
@login_required
def comment (post_id):
    print("postId:",post_id)
    note = Post.query.filter_by(id = post_id).first()
    text = request.form.get('text')
    print(text)
    if not text :
        
        flash("empty comment ",category='error')
    else:
        if note:
            comment = Comment(
            text=text, user_id=current_user.id, post_id=note.id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')
    return redirect('/')
   
    
#like
@views.route("/like-post/<post_id>",methods=['POST','GET'])
@login_required
def post_like(post_id):
    # note = json.loads(request.data)
    # post_id = note['noteId']
    
    post =Post.query.filter_by(id=post_id).first()
    like=  Post_like.query.filter_by(user_id=current_user.id,post_id=post_id).first()
    print("work1")
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
        
    elif like:
        print(like)
        db.session.delete(like)
        db.session.commit()
        

    else:
        print("work3")
        like= Post_like(user_id=current_user.id,post_id=post_id)
        db.session.add(like)
        db.session.commit()
        

        
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.user_id, post.likes)})


#Delete Note
@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
  
    post = json.loads(request.data)
    post_id = post['postId']
    
    post = Post.query.get(post_id)
    comments = post.comments
    likes=post.likes
        
    for like in likes:
        id = like.id
        post_like=Post_like.query.get(id)
        db.session.delete(post_like)
        db.session.commit()
    for comment in comments:
        id = comment.id 
        post_comment=Comment.query.get(id)
        db.session.delete(post_comment)
        db.session.commit()
        
    if post.img_name != None:
        path = app.config['POST_FOLDER'] + post.img_name
        os.remove(path)
        

    if post:

        if post.user_id == current_user.id or session["user_id"] == 1:
            db.session.delete(post)
            db.session.commit()
    return jsonify()



#profile
@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form =Profileupdate()

    user = user = User.query.get(current_user.id)  

    images = user.profile_pic

    if  request.method == 'POST':
        # user_name = request.form.get('username')
        bio = request.form.get('bio')
        name = request.form.get('fullname')
        pic = request.files['image']
        # userName=User.query.filter_by(user_name=user_name).first()

        if len(name) < 1:
            flash('Name is too short!', category='error')
            return redirect('/profile')

        elif len(bio) < 1:
            flash('BIO is too short!', category='error')
            return redirect('/profile')
        

        else:
            if pic and allowed_file(pic.filename) :

                filename = secure_filename(pic.filename)
                num = str(randint(00000000, 99999999))
                user = current_user
                pic_name = str(uuid.uuid1()) + "_" + num + "_" + filename
                print("filename:", pic_name)
                try:
                    img = user.profile_pic
                    print("Profile Name:", img)

                    if img != "Default/Default.jpeg":
                        print("imageName:", img)
                        
                        path = app.config['UPLOAD_FOLDER'] + img
                        os.remove(path)
                       
                        user.bio = bio
                        user.name = name
                        user.profile_pic = pic_name
                        db.session.commit()
                        flash("Pic_added")
                        pic.save(
                            os.path.join(app.config['UPLOAD_FOLDER'],
                                         pic_name))
                        return redirect('/profile')

                    elif img == "Default/Default.jpeg":
                       
                        user.bio = bio
                        user.name = name
                        user.profile_pic = pic_name
                        db.session.commit()
                        flash("Pic_added")
                        pic.save(
                            os.path.join(app.config['UPLOAD_FOLDER'],
                                         pic_name))
                        return redirect('/profile')

                except:
                    flash("Somthing error", category="error")

            else:
               
                user.bio = bio
                user.name = name
                db.session.commit()
                # flash('Images only!',category='error')
                

    return render_template('profile.html', images=images,form=form)





#Remove Profile
@views.route('/remove-Profile-photo', methods=['POST', 'GET'])
@login_required
def remove_Profile_photo ():
    if current_user.profile_pic == 'Default/Default.jpeg':

        return redirect('/profile')
    
    else:
        path = app.config['UPLOAD_FOLDER'] + current_user.profile_pic
        current_user.profile_pic='Default/Default.jpeg'
        db.session.commit()
        os.remove(path)
        return redirect('/profile')
    

#admin login
@views.route('/admin-login', methods=['POST', 'GET'])
@login_required
def admin_login():   
    form = LoginForm()
    
    

    
    if current_user.admin == True:
        admin = Admin.query.filter_by(user_id=current_user.id).first()
        if request.method == "POST":
            email = request.form.get('email')
            password=request.form.get('password')
            admin_data = Admin.query.filter_by(email=email).first()  #check email from db
            print(email)
            if admin_data:
                if check_password_hash(admin_data.password,password):  #check the password from db
                    if admin_data.user_id == current_user.id:
                        session.permanent = True
                        
                        session[f"admin_login{current_user.id}"]=admin_data.user_id
                        
                        flash('Logged in successfully!', category='success')
                        return redirect(url_for('views.admin'))
                    else:
                        flash('you cannot use other admin ID ', category='success')
                        return redirect(url_for('views.admin'))
        return render_template('login.html',admin=admin,form=form)
    else:
        flash("User muste be a admin for access this page")
        return redirect(url_for('views.home'))

# logut Admin
@views.route('logout-admin', methods=['GET'])
@login_required
def logout_admin():
    
    if  f"admin_login{current_user.id}" in session  : 
        if session[f"admin_login{current_user.id}"] == current_user.id:
            session.pop(f"admin_login{current_user.id}", None)
        else:
            return flash(f"somthing error {current_user.id} ")
    return redirect(url_for('views.home'))
    



#admin
@views.route('/admin', methods=['POST', 'GET'])
@login_required
def admin(): 
    form= SearchForm()
        
    if  f"admin_login{current_user.id}" in session :       
        if current_user.admin  == True and session[f"admin_login{current_user.id}"] == current_user.id: 
            user = User.query.order_by(User.date)     
            return render_template("Admin.html", user=user,form =form)
        else:
            flash("User muste be a admin for access this page")
            return redirect(url_for('views.admin_login'))
    elif current_user.id == 1 and current_user.admin == False:
        user = User.query.get(1)   
        add_admin =Admin(user_id=user.id,email=user.email,password=user.password)
        db.session.add(add_admin)
        user.admin =True
        db.session.commit()
        return redirect(url_for('views.admin_login'))
        
    else:        
        flash("User muste be a admin for access this page")
        return redirect(url_for('views.admin_login'))
        
        


#add admin
@views.route('/add-admin', methods=['POST'])
@login_required
def add_admin():
    if current_user.id ==1:
        user = json.loads(request.data)
        userID = user['userId']
        user = User.query.get(userID)
        
    
                
        print("work")
        print(user.admin)
        add_admin =Admin(user_id=user.id,email=user.email,password=user.password)
        db.session.add(add_admin)
        user.admin =True
        db.session.commit()
        print(user.admin)

        return redirect('/admin')
    
    
    
#admin_details

@views.route('/admin-details', methods=['POST', 'GET'])
@login_required
def admin_details(): 
    form=Editadmin()
    if  f"admin_login{current_user.id}" in session :       
        if current_user.admin  == True and session[f"admin_login{current_user.id}"] == current_user.id:
            admin = Admin.query.filter_by(user_id=session[f"admin_login{current_user.id}"]).first()
            if  form.validate_on_submit( ) and request.method == 'POST':
                email = request.form.get('email')
                name = request.form.get('fullname')
                password=request.form.get('password1')
                password1=request.form.get('password2')
                email_check = Admin.query.filter_by(email=email).first()
                
                if len(email) < 1:
                    flash('email is too short!', category='error')
                    return redirect(url_for('views.admin_details'))
                elif password != password1:
                    flash('password don\'t macth.', category='error')
                    return redirect(url_for('views.admin_details'))
                
                else:
                    if admin.email != email:
                        if email_check:
                            flash('Email already exists', category='error')
                            return redirect(url_for('views.admin_details'))
                        else:
                            admin.email = email
                            admin.name = name
                            db.session.commit()
                            flash('Profile Updated')
                        return redirect(url_for('views.admin_details'))
                            
                    if password == None:
                        admin.email = email
                        admin.name = name
                        admin.password = generate_password_hash(password)
                        db.session.commit()
                        flash('Profile Updated')
                        return redirect(url_for('views.admin_details'))
                    
                    else:
                        admin.email = email
                        admin.name = name
                        db.session.commit()
                        flash('Profile Updated')
                        
            return render_template('editadmin.html',admin=admin,form=form)
#remove admin
@views.route('remove-admin',methods=['POST'])
@login_required
def remove_admin():
    user = json.loads(request.data)
    userID = user['userId']
    user = User.query.get(userID)
    
    admin = Admin.query.get(userID)
    db.session.delete(admin)
    user.admin=False
    db.session.commit()
    
    return redirect('/admin')


#search
@views.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    
    if f"admin_login{current_user.id}" in session or current_user.id == 1:  
        if current_user.admin  == True and session[f"admin_login{current_user.id}"] == current_user.id or current_user.id == 1:
            if request.method == 'POST':
                search = request.form.get('search')
                userid = User.query.filter_by(id=search).first()
                userEmail = User.query.filter_by(email=search).first()
                userName = User.query.filter_by(user_name=search).first()

                if userEmail:
                    #    User.query.get(userEmail)
                    user = userEmail

                    return render_template('search.html', user=user)

                elif userName:
                    user = userName

                    return render_template('search.html', user=user)
                elif userid:
                    user = userid

                    return render_template('search.html', user=user)
                else:
                    flash("User Not Found")
                    return redirect('/admin')
        return render_template('search.html')


#admin delete user
@views.route('/delete-user', methods=['POST'])
@login_required
def delete_user():
    if f"admin_login{current_user.id}" in session  or current_user.id == 1: 
        if current_user.admin  == True and session[f"admin_login{current_user.id}"] == current_user.id or current_user.id == 1:
            
            user = json.loads(request.data)
            userID = user['userId']
            print("id",userID)
            user = User.query.get(userID)
            posts = user.posts
            
            for post in posts:
                
                
                id = post.id
                
                note = Post.query.get_or_404(id)
                post_likes=note.likes
                comments=note.comments
            
                for like in post_likes:
                    print("likes:",like)
                    id = like.id
                    post_like=Post_like.query.get(id)
                    db.session.delete(post_like)
                    db.session.commit()
                                
                for comment in comments:
                    print("comment:",comment)
                    id = comment.id 
                    post_comment=Comment.query.get(id)
                    db.session.delete(post_comment)
                    db.session.commit()
                if post.img_name != None:
                    print("imgage2")
                    
                    path = app.config['POST_FOLDER'] + post.img_name
                    os.remove(path)
                    
                db.session.delete(post)
                db.session.commit()

            if user:
                img = user.profile_pic

                if img != "Default/Default.jpeg":
                    path = app.config['UPLOAD_FOLDER'] + img
                    db.session.delete(user)
                    db.session.commit()
                    os.remove(path)
                elif img == "Default/Default.jpeg":
                    print("workii")
                    db.session.delete(user)
                    db.session.commit()

        return redirect('/admin')

#admin edit user
@views.route('/edit-user/<int:id>', methods=['POST','GET'])
@login_required
def edit_user(id):
    form=Useredit()
    
    if f"admin_login{current_user.id}" in session  or current_user.id == 1: 
        if current_user.admin  == True and session[f"admin_login{current_user.id}"] == current_user.id or current_user.id == 1:
            user = User.query.get(id) 
            form.gender.default=user.gender
            form.process()
        if request.method == 'POST':
    
            email = request.form.get('email')
            user_name = request.form.get('username')        
            name = request.form.get('fullname')
            bio = request.form.get('bio')
            gender = request.form.get('gender')
      
            #User.query.filter_by(id=user.id).update(dict(email=email,user_name=user_name,name=name,bio=bio,gender=gender))
           
            
            userName = User.query.filter_by(user_name=user_name).first()
            if user.user_name == user_name:
                
                    
                    user.email=email
                    print("work1")
                    user.name=name
                    user.bio=bio
                    user.gender=gender
                    db.session.commit()        
                    flash("User Data updated")
                    return redirect('/admin')
            
            else:
                print(userName)
                if userName:
                    flash("User Name already exiets")
                    return redirect(url_for('views.edit_user',id=id))
                user.user_name=user_name
                user.email=email
                user.name=name
                user.bio=bio
                user.gender=gender
                db.session.commit()        
                flash("User Datae updated")
                return redirect('/admin')
                    
    
        return render_template('edituser.html',user=user,form=form)
        

#admin createuser
@views.route('/createuser', methods=['POST', 'GET'])
@login_required
def createuser():
    form = SingupForm()
    if f"admin_login{current_user.id}" in session  or current_user.id == 1: 
        if current_user.admin  == True and session[f"admin_login{current_user.id}"] == current_user.id or current_user.id == 1:
            if form.validate_on_submit() and request.method == 'POST':
                email = form.email.data
                user_name = form.username.data
                password1 = form.password1.data
                password2 = form.password2.data
                gender = form.gender.data
                
                user = User.query.filter_by(email=email).first()
                userName = User.query.filter_by(user_name=user_name).first()

                if user:
                    flash('Email already exiets', category='error')
                    return redirect('/sign-up')

                elif userName:
                    print(user_name)
                    flash('User Name already exiets', category='error')
                    return redirect('/sign-up')
                
                elif password1 != password2:
                    flash('password don\'t macth.', category='error')
                    return redirect('/sign-up')
                elif gender == None:
                    flash(
                        'Select Your Gender',
                        category='error')
                    return redirect('/sign-up')
                else:
                    adduser= User(email=email,user_name=user_name,password=(generate_password_hash(password1)),gender=gender)
                    db.session.add(adduser)
                    db.session.commit()
                    flash("New user Added")
                    return redirect(url_for('views.admin'))
    return redirect(url_for('views.admin'))

