from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        data=[
            {"description": "Fix the sink"},
            {"description": "Walk the dog"},
            {"description": "Flush the toilet"},
        ],
    )
