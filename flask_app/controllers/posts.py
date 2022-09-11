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
        return redirect('/dashboard')
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
def create():
    posts = Post.get_all_posts()
    return render_template("new.html",posts=posts)


# make sure to add <int:> here
@app.route('/post/view/<int:id>')
def show(id):
    data = {
        "id": id
    }
    return render_template("recipe.html")

@app.route('/post/edit/<int:id>')
def edit(id):
    data = {
        "id": id
    }
    post = Post.get_by_way_of_id(data)
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