from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:test4Echo@localhost:5432/todoapp2'
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    description = db.Column(db.String(), nullable = False)
    completed = db.Column(db.Boolean, nullable = False, default = False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

class TodoList(db.Model):
    __tablename__= 'todolist'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

#db.create_all()

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_complete_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })


@app.route('/')
def index():
    return render_template('index.html', data = Todo.query.order_by('id').all())

@app.route('/todos/create', methods = ['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if not error:
        return jsonify(body)






