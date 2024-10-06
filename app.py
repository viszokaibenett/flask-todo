# Imports - flask, render_template, SQLAlchemy, request, redirect, url_for
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for

app = Flask(__name__)

# Database

# Path to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating the database
db = SQLAlchemy(app)

# Creating a class for the todo items
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100)) # Max char number will be 100
    complete = db.Column(db.Boolean)

with app.app_context():
        db.create_all()

# Routing - defining different URLs

# Index page
@app.route('/')
def index():
    # Show all todos - querying the database
    todo_list = Todo.query.all() # This returns a list with all items
    print(todo_list)
    return render_template('base.html', todo_list = todo_list)

# Add todo items
@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title') # Title comes from the html - input name="title"
    new_todo = Todo(title=title, complete=False) # Title will be title, and it will be not completed
    db.session.add(new_todo) # Adding to the database
    db.session.commit()
    return redirect(url_for('index')) # After adding refreshing the index page

# Update todo items
@app.route('/update/<int:todo_id>') # int - integer: todo_id -> specifying which todo to edit
def update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() # Only querying the item which will be updated
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

# Deleting todo items
@app.route('/delete/<int:todo_id>') # int - integer: todo_id -> specifying which todo to edit
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first() # Only querying the item which will be updated
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()

    app.run(debug=True)