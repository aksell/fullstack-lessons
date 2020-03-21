from flask import Flask, render_template, request, redirect, url_for
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
    db.session.add(TodoItem(description=request.form["description"]))
    db.session.commit()
    return redirect(url_for("index"))  # name of method we want to redirec to
