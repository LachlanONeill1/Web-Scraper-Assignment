import plotly.graph_objects as go
import yfinance as yf
import mplfinance as mpf
import datetime as dt
import matplotlib.pyplot as plt
class Graph():
    def __init__(self, crypto_symbol):
        start = dt.datetime(2024,1,1)
        end = dt.datetime.now()

        data = yf.download(crypto_symbol, start=start, end=end)
        mpf.plot(data, type="candle", style="yahoo")