from flask import Flask, render_template
import yfinance as yf
import plotly.graph_objects as go
import os # NEW: To access environment variables
from newsapi import NewsApiClient # NEW: To use the NewsAPI

app = Flask(__name__)

# NEW: Initialize the NewsAPI client
# This safely reads the API key from the environment variables you set in Render
newsapi = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY'))

@app.route('/')
def index():
    return """
    <h1>Welcome to the Market Dashboard</h1>
    <p>Try appending a stock symbol to the URL, like this:</p>
    <ul>
        <li><a href="/dashboard/AAPL">/dashboard/AAPL</a></li>
        <li><a href="/dashboard/TSLA">/dashboard/TSLA</a></li>
        <li><a href="/dashboard/MSFT">/dashboard/MSFT</a></li>
    </ul>
    """

@app.route('/dashboard/<symbol>')
def home(symbol):
    # --- Part 1: "At-a-Glance" Panel Data ---
    ticker = yf.Ticker(symbol)
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
        data=[go.Candlestick(x=hist_df.index, open=hist_df['Open'], high=hist_df['High'], low=hist_df['Low'], close=hist_df['Close'])]
    )
    fig.update_layout(title=f'{symbol.upper()} 5-Minute Candlestick Chart', yaxis_title='Stock Price (USD)', xaxis_title='Time', xaxis_rangeslider_visible=False)
    chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # --- NEW: Part 3: Fetch Top Financial News ---
    # Get the top 5 financial headlines from US sources
    top_headlines = newsapi.get_top_headlines(
        category='business',
        language='en',
        country='us',
        page_size=5
    )
    # Get the list of articles from the response
    articles = top_headlines.get('articles', [])

    # --- Part 4: Render the template ---
    # Pass the articles list to the template
    return render_template('index.html', stats=stats, chart_html=chart_html, symbol=symbol, articles=articles)