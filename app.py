from flask import Flask, render_template
import yfinance as yf # Import the yfinance library

# This creates the Flask web server application.
app = Flask(__name__)

# This is the main "route" for our application.
@app.route('/')
def home():
    """
    This function runs when someone visits the main page of the website.
    """
    # NEW: Create a ticker object for Apple
    ticker = yf.Ticker("AAPL")

    # NEW: Get the stock info dictionary
    info = ticker.info

    # NEW: Create a dictionary for the stats we want.
    # We use .get() to avoid errors if a key doesn't exist.
    stats = {
        'previous_close': info.get('previousClose', 'N/A'),
        'open': info.get('open', 'N/A'),
        'day_high': info.get('dayHigh', 'N/A'),
        'day_low': info.get('dayLow', 'N/A'),
        'volume': f"{info.get('volume', 0):,}" # Format with commas
    }

    # OLD: return render_template('index.html')
    # NEW: Pass the stats dictionary to the template
    return render_template('index.html', stats=stats)