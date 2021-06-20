import matplotlib.pyplot as plt
from Investar.MarketDB import MarketDB

class BollingerBand:
    def __init__(self):
        print()

    def get_bollinger_band(self, company, start_date):
        mk = MarketDB()
        df = mk.get_daily_price(company, start_date)

        df['MA20'] = df['close'].rolling(window=20).mean()
        df['stddev'] = df['close'].rolling(window=20).std()
        df['upper'] = df['MA20'] + (df['stddev'] * 2)
        df['lower'] = df['MA20'] - (df['stddev'] * 2)
        df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])
        df['bandwidth'] = (df['upper'] - df['lower']) / df['MA20'] * 100
        df = df[19:]
        return df

    def show_bollinger_chart(self, df, company):
        plt.plot(df.index, df['close'], color='#0000ff', label='Close')
        plt.plot(df.index, df['upper'], 'r--', label='Upper band')
        plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
        plt.plot(df.index, df['lower'], 'c--', label='Lower Band')
        plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
        plt.legend(loc='best')
        plt.xticks(rotation=45)
        str = company + ' Bollinger Band (20 Day, 2 Std)'
        plt.title(str)

    def show_pb_chart(self, df, mgnif):
        _str = '%B'+'x'+str(mgnif)
        plt.plot(df.index, df['PB'] * mgnif, color='b', label=_str)
        plt.grid(linestyle='dotted')
        plt.legend(loc='best')
        plt.xticks(rotation=45)

    def show_bandwidth_chart(self, df):
        plt.plot(df.index, df['bandwidth'], color='m', label='bandwidth')
        plt.grid(linestyle='dotted')
        plt.legend(loc='best')
        plt.xticks(rotation=45)






