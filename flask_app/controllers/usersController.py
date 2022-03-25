from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.posts import Post
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

from werkzeug.utils import secure_filename
import os
#podria haber pag principal


#REGISTER ---------------------------------------------------------------
@app.route("/sign-up")
def sign_up():
    return render_template('sign-up.html')

@app.route("/sign_up", methods=['POST'])
def redirect_sign_up():
    return render_template('sign-up.html')

@app.route("/register", methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/sign-up')

    # image1 = request.files['default_profile_image']
    # nombre_image1 = secure_filename(image1.filename)
    # image1.save(os,)

    #Data to send:
    #default_profile_image = secure_filename(request.files['default_profile_image'].filename)
    #default_profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'],

    pwd = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "name": request.form['name'],
        "username": request.form['username'],
        "email": request.form['email'],
        "password": pwd,
        "bio": "",
        "profile_image": 'default_profile_image.png',
        "bg_image": 'default_bg_image.png'
    }
    id = User.create_user(data)
    print('---------------------')
    print(id)
    #Session starts
    session['user_id'] = id
    return redirect('/dashboard')


#LOGIN -----------------------------------------------------------------

@app.route("/sign-in")
def sign_in():
    return render_template('sign-in.html')

@app.route("/sign_in", methods=['POST'])
def redirect_sign_in():
    return render_template('sign-in.html')

@app.route("/login", methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Email not found", "login")
        return redirect('/sign-in')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect Password", "login")
        return redirect('/sign-in')

    #Session starts
    session['user_id'] = user.id
    return redirect('/dashboard')


#DASHBOARD ------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/sign-in')

    data = {
        "id": session['user_id']
    }
    print(session['user_id'])
    print('******************************************************************')
    user = User.get_user_by_id(data)
    users = User.get_all_users()

    #posts = Post.get_all_posts()
    posts_with_info = Post.get_all_posts_with_info()
    print(users)
    #return render_template('dashboard.html',users=users, user=user)
    return render_template('dashboard.html', user=user,users=users,posts=posts_with_info)

#LOGOUT -------------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/sign-in')




#PROFILE
#Esta conexion debe ir con el boton de user en home
@app.route('/profile/<string:username>')
def show_one_user(username):
    if 'user_id' not in session:
        return redirect('/dashboard')

    data = {
        "username": username
    }
    user= User.get_user_by_username(data)
    users = User.get_all_users()
    #enviarle all posts tb
    posts_with_info = Post.get_all_posts_with_info()
    return render_template('profile.html',user=user, users=users, posts=posts_with_info)

@app.route('/profile/<string:username>/edit', methods=['POST'])
def edit_one_user(username):
    if 'user_id' not in session:
        return redirect('/dashboard')

    data = {
        "username": username
    }
    user= User.get_user_by_username(data)
    users = User.get_all_users()
    #enviarle all posts tb
    #posts_with_info = Post.get_all_posts_with_info()
    return render_template('edit.html',user=user, users=users)

@app.route('/profile/update', methods=['POST'])
def update_one_user():
    if 'user_id' not in session:
        return redirect('/sign-in')

    # if not User.validate_user(request.form):
    #         return redirect('/dashboard')

    if 'bg_image' or 'profile_image' not in request.files:
        flash('Image not found','edit')
        return '<script>document.location.href = document.referrer</script>'

    bg_image = request.files['bg_image']
    profile_image = request.files['profile_image']

    if bg_image or profile_image == '':
        flash('The name of a file is empty','edit')
        return '<script>document.location.href = document.referrer</script>'

    name_bg_image = secure_filename(bg_image.filename)
    name_profile_image = secure_filename(profile_image.filename)

    bg_image.save(os.path.join(app.config['UPLOAD_FOLDER'], name_bg_image))
    profile_image.save(os.path.join(app.config['UPLOAD_FOLDER'], name_profile_image))

    data = {
        "id":request.form['id'],
        "name": request.form['name'],
        "bio" :request.form['bio'],
        "bg_image": name_bg_image,
        "profile_image": name_profile_image,
    }
    User.update_user(data)
    return redirect('/dashboard')