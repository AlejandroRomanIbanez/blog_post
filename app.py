from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_post/blog_posts.json', 'r') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


def generate_id():
    if not blog_posts:
        return 1
    else:
        existing_ids = [post['id'] for post in blog_posts]
        return max(existing_ids) + 1

blog_posts = []


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        new_post = {
            'id': generate_id(),
            'author': author,
            'title': title,
            'content': content
        }
        blog_posts.append(new_post)
        with open('blog_post/blog_posts.json', 'w') as file:
            json.dump(blog_posts, file)
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    app.run()
