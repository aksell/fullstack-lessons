from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgres://postgres:postgres@localhost:5432/todoapp"  # dblang://user:pswd@ip:port/database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class TodoList(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    todos = db.relationship("TodoItem", backref="list", lazy=True)

    def __repr__(self):
        return f"TODO List: {self.name}"


class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey("todolist.id"), nullable=False)

    def __repr__(self):
        return f"id: {self.id} description: {self.description}"


@app.route("/list/<list_id>")
def get_list_todos(list_id):
    return render_template(
        "index.html",
        lists=TodoList.query.all(),
        active_list=TodoList.query.get(list_id),
        todos=TodoItem.query.filter_by(list_id=list_id).order_by("id").all(),
    )


@app.route("/")
def index():
    return redirect(url_for("get_list_todos", list_id=1))


@app.route("/todo/create", methods=["POST"])
def handle_create_todo():
    description = request.get_json()["description"]
    todo = TodoItem(description=description)
    error = False
    try:
        db.session.add(todo)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        if error:
            abort(
                400
            )  # Route handlers should always return something or raise an exception never stay silent
        else:  # Should not use todo item after closing because it would not be attached to a session
            return jsonify({"description": todo.description})
        db.session.close()  # Is this ever executed?


@app.route("/todo/<todo_id>/delete", methods=["DELETE"])
def delete_todo(todo_id):
    try:
        item = TodoItem.query.get(todo_id)
        db.session.delete(item)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return jsonify({"id": todo_id})


@app.route("/todo/<todo_id>/update-checked", methods=["POST"])
def handle_checked_update(todo_id):
    try:
        checked = request.get_json()["completed"]
        item = TodoItem.query.get(todo_id)
        item.completed = True
        db.session.commit()
    except:
        abort(400)
    finally:
        db.session.close()
    return redirect(url_for("index"))
