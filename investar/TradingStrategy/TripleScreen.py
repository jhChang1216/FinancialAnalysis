import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from Investar.MarketDB import MarketDB

class TripleScreen():

    def __init__(self, company, start_date):
        mk = MarketDB()
        self.df = mk.get_daily_price(company, start_date)
        self.company = company
        self.ohlc = pd.DataFrame()

    def get_market_tide(self):
        df = self.df
        ema60 = df.close.ewm(span=60).mean()
        ema130 = df.close.ewm(span=130).mean()
        macd = ema60 - ema130
        signal = macd.ewm(span=45).mean()
        macdhist = macd - signal

        df = df.assign(ema130=ema130, ema60 = ema60, macd = macd,
                           signal = signal, macdhist=macdhist).dropna()
        df['number'] = df.index.map(mdates.date2num)
        ohlc = df[['number', 'open', 'high', 'low', 'close']]
        ohlc.index = pd.to_datetime(ohlc.index)
        self.ohlc = ohlc
        self.df = df
        return

    def get_market_wave(self):
        df = self.df
        ndays_high = df.high.rolling(window=14, min_periods=1).max()
        ndays_low = df.low.rolling(window=14, min_periods=1).min()
        fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100
        slow_d = fast_k.rolling(window=3).mean()
        df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()
        self.df = df
        return

    def show_candle_chart(self,subplot):
        df = self.df
        plt.title('Candle & MACD Chart')
        plt.grid(linestyle = "dotted")
        candlestick_ohlc(subplot, self.ohlc.values, width=.6, colorup='red', colordown='blue')
        subplot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.plot(df.number, df['ema130'], color='c', label = 'EMA130')
        plt.legend(loc='best')

    def show_macd_chart(self, subplot):
        df = self.df
        subplot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.bar(df.number, df['macdhist'], color='m', label='MACD-hist')
        plt.plot(df.number, df['macd'], color='b', label='MACD')
        plt.plot(df.number, df['signal'], 'g--', label='MACD-signal')
        plt.legend(loc='best')

    def show_stochastic_chart(self, subplot):
        df = self.df
        subplot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.plot(df.number, df['fast_k'], color ='c', label='%K')
        plt.plot(df.number, df['slow_d'], color = 'k', label='%D')
        plt.yticks([0, 20, 80, 100])
        plt.legend(loc='best')

    def sim_trade(self):
        account = 1000000
        stocks = 0
        profit = 0

        df = self.df
        for i in range(len(df.close)):
            if df.ema130.values[i-1] < df.ema130.values[i] and \
                df.slow_d.values[i-1] >= 20 and df.slow_d.values[i] < 20:
                account -= df.close.values[i]
                stocks += 1
                print(f"[{df.index.values[i]}] 매수 체결 - 매수가 : {df.close.values[i]} | "
                      f"체결 수량 : 1 | 현재 총 {stocks} 주")
            elif df.ema130.values[i-1] > df.ema130.values[i] and \
                df.slow_d.values[i-1] <= 80 and df.slow_d.values[i] > 80:
                if stocks == 0:
                    continue
                print(f"[{df.index.values[i]}] 매도 체결 - 매도가 : {df.close.values[i]} |"
                      f"체결 수량 : {stocks} | 현재 총 0 주")
                account += stocks * df.close.values[i]
                stocks = 0

        profit = account + df.close.values[len(df.close)-1] * stocks - 1000000
        print(f"삼중창 매매법 총 수익 : {profit} (원)")



