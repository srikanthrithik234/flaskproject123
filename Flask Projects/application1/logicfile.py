from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    with sqlite3.connect("pfsdskill.db") as conn:
        c = conn.cursor()
        # Create table for blog posts
        c.execute('''CREATE TABLE IF NOT EXISTS blog_posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        date_posted TEXT NOT NULL
                    )''')
        # Create table for to-do items
        c.execute('''CREATE TABLE IF NOT EXISTS todo_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT NOT NULL,
                        date_created TEXT NOT NULL
                    )''')
        conn.commit()

# Route to view all blog posts
@app.route('/blog')
def view_blog():
    with sqlite3.connect("pfsdskill.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM blog_posts ORDER BY date_posted DESC")
        posts = c.fetchall()
    return render_template('view_blog.html', posts=posts)

# Route to add a new blog post
@app.route('/blog/new', methods=['GET', 'POST'])
def add_blog_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date_posted = datetime.now().strftime('%Y-%m-%d %H:%M')

        with sqlite3.connect("pfsdskill.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO blog_posts (title, content, date_posted) VALUES (?, ?, ?)",
                      (title, content, date_posted))
            conn.commit()
        return redirect(url_for('view_blog'))
    return render_template('add_blog_post.html')


@app.route('/todo')
def view_todo():
    with sqlite3.connect("pfsdskill.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM todo_items ORDER BY date_created DESC")
        tasks = c.fetchall()
    return render_template('view_todo.html', tasks=tasks)

# Route to add a new to-do item
@app.route('/todo/new', methods=['GET', 'POST'])
def add_todo_item():
    if request.method == 'POST':
        task = request.form['task']
        date_created = datetime.now().strftime('%Y-%m-%d %H:%M')

        with sqlite3.connect("pfsdskill.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO todo_items (task, date_created) VALUES (?, ?)",
                      (task, date_created))
            conn.commit()
        return redirect(url_for('view_todo'))
    return render_template('add_todo_item.html')

# Route to delete a to-do item
@app.route('/todo/delete/<int:id>')
def delete_todo_item(id):
    with sqlite3.connect("pfsdskill.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM todo_items WHERE id = ?", (id,))
        conn.commit()
    return redirect(url_for('view_todo'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
