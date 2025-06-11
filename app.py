from flask import Flask, render_template

# This creates the Flask web server application.
app = Flask(__name__)

# This is the main "route" for our application.
# The '@' symbol makes the function below it a web page.
@app.route('/')
def home():
    """
    This function runs when someone visits the main page of the website.
    """
    # It just loads and returns the index.html file.
    return render_template('index.html')