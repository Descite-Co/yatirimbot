"""Flask application for a web server."""

from threading import Thread
from flask import Flask, render_template, url_for

app = Flask("")

@app.route("/", methods=["GET", "POST"])
def home():
    """Render the home page."""
    return render_template("index.html")

def run():
    """Run the Flask application."""
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    """Start the Flask application in a separate thread."""
    t = Thread(target=run)
    t.start()
