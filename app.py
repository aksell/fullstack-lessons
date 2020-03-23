from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgres://postgres:postgres@localhost:5432/todoapp"  # dblang://user:pswd@ip:port/database

db = SQLAlchemy(app)


class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"id: {self.id} description: {self.description}"


db.create_all()


@app.route("/")
def index():
    return render_template("index.html", data=TodoItem.query.all())


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
        db.session.close()
