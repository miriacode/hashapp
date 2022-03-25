from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.posts import Post

#CREATE -----------------------------------------------------
# @app.route('/posts/new')
# def new_posts():
#     return render_template('add_recipe.html')

@app.route('/post/create', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/sign-in')

    if not Post.validate_post(request.form):
        return redirect('/dashboard')
    data = {
        "content": request.form['content'],
        "owner_id": session['user_id']
    }
    
    Post.create_post(data)
    return redirect('/dashboard')



#Aqui poner in adavent listener 
#https://stackoverflow.com/questions/69040338/how-to-get-an-onclick-listener-to-work-with-python-flask
#SHOW -----------------------------------------------------------------
@app.route('/post/<int:id>')
def show_post(id):
    if 'user_id' not in session:
        return redirect('/dashboard')


    data = {
            "id": id
        }
    #post = Post.get_post_with_info_by_id(data)
    post = Post.get_post_by_id(data)


    data2 = {
        "id": post.owner_id
    }
    user= User.get_user_by_id(data2)
    print('0000000000000000000000000000000000000000')
    print(user)
    
    


    return render_template('post.html', post=post, user=user)




# @app.route('/dash')
# def show_one_usere():
   
#     return render_template('dashboard.html')