from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

with open('blog_post/blog_posts.json', 'r') as file:
    blog_posts = json.load(file)
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
            json.dump(blog_posts, file, indent=4)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    if request.method == 'POST':
        with open('blog_post/blog_posts.json', 'r') as file:
            blog_posts = json.load(file)
        for post in blog_posts:
            if post['id'] == post_id:
                blog_posts.remove(post)
                break
        with open('blog_post/blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)
        return redirect(url_for('index'))

    return render_template('delete.html', post_id=post_id)


def update(post_id, blog_posts):
    post_id = int(post_id)

    index = next((index for index, post in enumerate(blog_posts) if post['id'] == post_id), None)

    if index is None:
        return "Post not found", 404

    if request.method == 'GET':
        return render_template('update.html', post=blog_posts[index])

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        blog_posts[index]['author'] = author
        blog_posts[index]['title'] = title
        blog_posts[index]['content'] = content

        with open('blog_post/blog_posts.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)
        return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    with open('blog_post/blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    return update(post_id, blog_posts)

@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    with open('blog_post/blog_posts.json', 'r') as file:
        blog_posts = json.load(file)

    # Find the post with the specified post_id
    for post in blog_posts:
        if post['id'] == post_id:
            # Increment the likes count for the post
            if 'likes' not in post:
                post['likes'] = 0
            post['likes'] += 1
            break

    # Update the blog_posts.json file with the updated data
    with open('blog_post/blog_posts.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run()
