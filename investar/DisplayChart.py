import mplfinance as mpf

def displayChart(company, df):
    kwargs = dict(title = company, type = 'candle',
                  mav=(2,4,6), volume=True, ylabel = 'ohlc candles')
    mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
    s = mpf.make_mpf_style(marketcolors=mc)
    mpf.plot(df, **kwargs, style=s)