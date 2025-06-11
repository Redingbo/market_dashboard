from flask import Flask, render_template
import yfinance as yf
import plotly.graph_objects as go # NEW: Import plotly graph objects

app = Flask(__name__)

@app.route('/')
def home():
    """
    This function runs when someone visits the main page of the website.
    """
    # --- Part 1: "At-a-Glance" Panel Data ---
    ticker = yf.Ticker("AAPL")
    info = ticker.info
    stats = {
        'previous_close': info.get('previousClose', 'N/A'),
        'open': info.get('open', 'N/A'),
        'day_high': info.get('dayHigh', 'N/A'),
        'day_low': info.get('dayLow', 'N/A'),
        'volume': f"{info.get('volume', 0):,}"
    }

    # --- NEW: Part 2: Interactive Candlestick Chart ---
    # Fetch 1 day of data at a 5-minute interval
    hist_df = ticker.history(period="1d", interval="5m")

    # Create the plotly figure
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=hist_df.index,
                open=hist_df['Open'],
                high=hist_df['High'],
                low=hist_df['Low'],
                close=hist_df['Close']
            )
        ]
    )

    # Update the layout for a cleaner look
    fig.update_layout(
        title='AAPL 5-Minute Candlestick Chart',
        yaxis_title='Stock Price (USD)',
        xaxis_title='Time',
        xaxis_rangeslider_visible=False # Hides the bulky range slider
    )

    # Convert the figure to an HTML div
    # include_plotlyjs='cdn' loads the JS from a remote source to keep our app light
    # full_html=False makes it a component, not a full page
    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')


    # --- Part 3: Render the template ---
    # Pass both the stats and the chart HTML to the template
    return render_template('index.html', stats=stats, chart_html=chart_html)