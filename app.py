from flask import Flask, render_template
import yfinance as yf
import plotly.graph_objects as go

app = Flask(__name__)

# NEW: A simple home page route
@app.route('/')
def index():
    # A simple message and a link to an example dashboard
    return """
    <h1>Welcome to the Market Dashboard</h1>
    <p>Try appending a stock symbol to the URL, like this:</p>
    <ul>
        <li><a href="/dashboard/AAPL">/dashboard/AAPL</a></li>
        <li><a href="/dashboard/TSLA">/dashboard/TSLA</a></li>
        <li><a href="/dashboard/MSFT">/dashboard/MSFT</a></li>
    </ul>
    """

# NEW: The dynamic route for our dashboard
@app.route('/dashboard/<symbol>')
def home(symbol): # NEW: The function now accepts the 'symbol' from the URL
    """
    This function runs when someone visits a dynamic dashboard page.
    """
    # --- Part 1: "At-a-Glance" Panel Data ---
    ticker = yf.Ticker(symbol) # NEW: Use the symbol from the URL
    info = ticker.info
    stats = {
        'previous_close': info.get('previousClose', 'N/A'),
        'open': info.get('open', 'N/A'),
        'day_high': info.get('dayHigh', 'N/A'),
        'day_low': info.get('dayLow', 'N/A'),
        'volume': f"{info.get('volume', 0):,}"
    }

    # --- Part 2: Interactive Candlestick Chart ---
    hist_df = ticker.history(period="1d", interval="5m")
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
    
    # NEW: Use the symbol variable in the title
    fig.update_layout(
        title=f'{symbol.upper()} 5-Minute Candlestick Chart',
        yaxis_title='Stock Price (USD)',
        xaxis_title='Time',
        xaxis_rangeslider_visible=False
    )

    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # --- Part 3: Render the template ---
    # NEW: Pass the symbol to the template as well
    return render_template('index.html', stats=stats, chart_html=chart_html, symbol=symbol)