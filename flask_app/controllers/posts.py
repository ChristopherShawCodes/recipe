from flask import render_template, request , redirect ,session, flash

from flask_app import app

from flask_app.models.user import User
from flask_app.models.post import Post

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/publish_post', methods=['POST'])
def publish_post():
    if 'user_id' not in session:
        return redirect('/')
    if not Post.validate_post(request.form):
        return redirect('/recipes/new')
    data = {
        "user_id": session['user_id'],
        "content": request.form['content'],
        "instructions": request.form['instructions'],
        "date_cooked": request.form['date_cooked'],
        "under_30": request.form['under_30'],
        "name": request.form['name'],
        # "created_at": request.form['created_at'],
        # "updated_at": request.form['updated_at'],
        # "user_id": request.form['user_id']
    }
    # new_post = Post.get_last()
    Post.publish(data)
    print(data)
    return redirect('/dashboard')


@app.route('/post/destroy/<int:id>')
def destroy(id):
    data = {
        "id":id
    }
    Post.destroy(data)
    return redirect('/dashboard')


@app.route('/recipes/new')
def new_recipe():
    posts = Post.get_all_posts()
    return render_template("new.html",posts=posts)


# make sure to add <int:> here
@app.route('/post/view/<int:id>')
def show(id):
    data = {
        "id": id
    }
    print(data)
    user_data = {
        "id": session["user_id"]
    }
    # post = Post.get_one(data)
    # all_posts = Post.get_all_posts()
    post = Post.get_one_post(data)
    user_instance = User.get_by_id(user_data)
    return render_template("recipe.html",post=post,user=user_instance)

@app.route('/post/edit/<int:id>')
def edit(id):
    data = {
        "id": id
    }
    post = Post.get_one(data)
    Post.publish(data)
    print(data)
    return render_template("edit.html",post=post)

@app.route('/post/update', methods = ['POST'])
def update():
    data = {
        "id":id
    }
    Post.update(data)
    print(data)
    return redirect("/dashboard")