from datetime import timedelta
import json
import os
from random import randint
import uuid
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask import session
from .models import Image, Image_like, User, Note,Post_like,Admin,Comment,ImageComment
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
        userId = current_user.id

        id = session["user_id"]
        if id == int(userId):
            user = current_user
            session["user_name"] = user.user_name
            notes = Note.query.order_by(Note.date)
            images = Image.query.order_by(Image.date)


            
    else:
        return redirect(url_for('auth.login'))

    return render_template('home.html',images=images,notes=notes)


#My post
@views.route('/my_post', methods=['GET', 'POST'])
@login_required
def my_post():
    
    image = current_user.images
    print(image)
    note = current_user.notes
    return render_template('my_post.html', notes=note, images=image)



#Createposts
@views.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    form= Createpost()
    if form.validate_on_submit():
                note = request.form.get('content')
                if len(note) < 1:
                    flash('Note is too short!', category='error')
                else:
                    new_note = Note(post=note, user_id=current_user.id)
                    db.session.add(new_note)
                    db.session.commit()
                    flash('NOTE created!', category='success')
                    return redirect('/')
    return render_template('creat_post.html',form=form)

@views.route('/upload_img', methods=['POST'])
@login_required
def upload_img():
    pic = request.files['pic']
    caption = request.form.get('caption')
    print("caption:", caption)
    if pic.filename == '':
        flash('No image selected for uploading')
        return redirect('/potos')

    if pic and allowed_file(pic.filename):

        user_id = current_user.id

        filename = secure_filename(pic.filename)

        random_num = str(randint(0000000000, 9999999999))

        pic_name = str(uuid.uuid1()) + "_" + random_num + "_" + filename
        print("filename:", pic_name)

        pic.save(os.path.join(app.config['POST_FOLDER'], pic_name))

        mimetype = pic.mimetype
        # size=pic.bytes
        # print("size:",size)
        print("MIMe: ", mimetype)

        photo = Image(mimetype=mimetype,
                      img_name=pic_name,
                      caption=caption,
                      user_id=user_id)
        db.session.add(photo)
        db.session.commit()
        flash('Image added !', category='success')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')

    return redirect('/')


# editpage
@views.route('/edit_note/<int:id>', methods=['POST','GET'])
@login_required
def edit_note(id):
    form = Createpost()
    note = Note.query.get(id)
    form.content.data=note.post
    
    if current_user.id == note.user_id or current_user.admin == True:   
        
        return render_template('editpost.html',note=note,form=form)
    
    else:
        flash("you can't Edit other user post",category='error')
        return redirect(url_for('views.home'))

#Update post
@views.route('/update_note/<int:id>', methods=['POST','GET'])
@login_required
def update_note(id):
    note = Note.query.get(id)
    if current_user.id == note.user_id or current_user.admin == True:    
        
        if request.method == 'POST':
            post = request.form.get('content')
            print(post)
            if len(post) < 1 :
                flash('Note is too short!', category='error')
                return redirect(url_for('views.edit_note',id=note.id))
            else:
                print("yessss")
                Note.query.filter_by(id=note.id).update(dict(post=post,edited=True))
                db.session.commit()
                flash('NOTE update!', category='success')
    return redirect('/')
            
#comment post 
@views.route("/comment/<post_id>",methods=['POST','GET'])
@login_required
def comment (post_id):
    print("postId:",post_id)
    note = Note.query.filter_by(id = post_id).first()
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

#imagecomment
@views.route("/imgcomment/<post_id>",methods=['POST','GET'])
@login_required
def imgcomment (post_id):
    print("postId:",post_id)
    image = Image.query.filter_by(id = post_id).first()
    text = request.form.get('text')
    print(text)
    if not text :
        
        flash("empty comment ",category='error')
    else:
        if image:
            comment = ImageComment(
            text=text, user_id=current_user.id, post_id=image.id)
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
    
    post =Note.query.filter_by(id=post_id).first()
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




#img Post Like /img_post-like
@views.route('/img_post-like', methods=['GET', 'POST'])
@login_required
def img_post_like():
    img = json.loads(request.data)
    img_id= img["imgId"]
    image = Image.query.filter_by(id=img_id).first()
    like=Image_like.query.filter_by(user_id=current_user.id,post_id=img_id).first()
    
    if not image:
        flash("post does not exist",category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like= Image_like(post_id=img_id,user_id=current_user.id)
        db.session.add(like)
        db.session.commit()
    return redirect('/')

#Delete Note
@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    print("note")
    note = json.loads(request.data)
    noteID = note['noteId']
    print("type:", noteID)
    note = Note.query.get(noteID)
    comments = note.comments
    likes=note.likes
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
        
        

    if note:

        if note.user_id == current_user.id or session["user_id"] == 1:
            db.session.delete(note)
            db.session.commit()
    return jsonify()


#Delete Photo
@views.route('/delete-Img', methods=['POST'])
@login_required
def delete_img():
    user = current_user

    img = json.loads(request.data)
    imgID = img['imgId']
    img = Image.query.get(imgID)

    namee = img.img_name
    path = app.config['POST_FOLDER'] + namee
    
    likes = img.likes
    comments = img.comments
    for like in likes:
        id = like.id
        image_like=Image_like.query.get(id)
        db.session.delete(image_like)
        db.session.commit()
        
    for comment in comments:
        id = comment.id 
        post_comment=ImageComment.query.get(id)
        db.session.delete(post_comment)
        db.session.commit()
        
    print("nameeeeee:   ", namee)
    if img:
        if img.user_id == user.id or session["user_id"] == 1:
            db.session.delete(img)
            db.session.commit()
            os.remove(path)

    return redirect('/')


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
@views.route('/remove_Profile_photo', methods=['POST', 'GET'])
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
@views.route('/add_admin', methods=['POST'])
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

@views.route('/admin_details', methods=['POST', 'GET'])
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
@views.route('remove_admin',methods=['POST'])
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
@views.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    if f"admin_login{current_user.id}" in session  or current_user.id == 1: 
        if current_user.admin  == True and session[f"admin_login{current_user.id}"] == current_user.id or current_user.id == 1:
            
            user = json.loads(request.data)
            userID = user['userId']

            user = User.query.get(userID)
            print(user)
            
            images = user.images
            notes = user.notes
            
            for image in images:
                path = app.config['POST_FOLDER'] + image.img_name
                id = image.id
                photo = Image.query.get(id)
                image_likes=photo.likes
                comments = photo.comments
                for comment in comments:
                    id =comment.id
                    imgComment=ImageComment.query.get(id)
                    db.session.delete(imgComment)
                    db.session.commit()
                for like in image_likes:
                    id = like.id
                    image_like=Image_like.query.get(id)
                    db.session.delete(image_like)
                    db.session.commit()
                
                

                db.session.delete(photo)
                db.session.commit()

                os.remove(path)

            for note in notes:
                id = note.id
                note = Note.query.get(id)
                post_likes=note.likes
                comments=note.comments
            
                for like in post_likes:
                                id = like.id
                                post_like=Post_like.query.get(id)
                                db.session.delete(post_like)
                                db.session.commit()
                                
                for comment in comments:
                        id = comment.id 
                        post_comment=Comment.query.get(id)
                        db.session.delete(post_comment)
                        db.session.commit()
                
                db.session.delete(note)
                db.session.commit()

            if user:
                img = user.profile_pic

                if img != "Default/Default.jpeg":
                    path = app.config['UPLOAD_FOLDER'] + img
                    db.session.delete(user)
                    db.session.commit()
                    os.remove(path)
                elif img == "Default/Default.jpeg":
                    db.session.delete(user)
                    db.session.commit()

        return redirect('/admin')

#admin edit user
@views.route('/edit_user/<int:id>', methods=['POST','GET'])
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
    if f"admin_login{current_user.id}" in session  or current_user.id == 1: 
        if current_user.admin  == True and session[f"admin_login{current_user.id}"] == current_user.id or current_user.id == 1:
            if request.method == 'POST':
                email = request.form.get('email')
                user_name = request.form.get('UserName')
                password1 = request.form.get('password1')
                password2 = request.form.get('password2')
                gender = request.form.get('gender')
                
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

