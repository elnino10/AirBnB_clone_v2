#!/usr/bin/python3
"""script starts a Flask web application"""
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """root route that displays Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def home():
    """route for the hbnb home"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def var_text(text):
    """route takes variable text and displays it as output"""
    return f"C { escape(text.replace('_', ' ')) }"


@app.route("/python/<text>", strict_slashes=False)
def py_text(text):
    """route takes variable text and displays it as output"""
    return f"Python { escape(text.replace('_', ' ')) }"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
