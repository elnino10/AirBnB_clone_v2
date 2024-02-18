#!/usr/bin/python3
"""script starts a Flask web application"""
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    """root route that displays Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb_route():
    """route for the hbnb home"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_route(text):
    """route takes variable text and displays it as output"""
    return f"C { escape(text.replace('_', ' ')) }"


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python_route(text="is cool"):
    """route takes variable text and displays it as output"""
    return f"Python { escape(text.replace('_', ' ')) }"


@app.route("/number/<int:n>", strict_slashes=False)
def number_route(n):
    """display 'n is a number' only if n is an integer"""
    return f"{escape(n)} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """display a HTML page only if n is an integer"""
    return render_template("5-number.html", number=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
