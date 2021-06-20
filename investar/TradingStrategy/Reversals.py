import matplotlib.pyplot as plt

class ReversalsTrading():
    def __init__(self, company, start_date):
        self.buy_tim = []
        self.sell_tim = []
        self.account = 1000000
        self.stock = 0
        self.profit = 0

    def calc_II(self, df):
        df['II'] = (2*df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) *df['volume']
        df['IIP21'] = df['II'].rolling(window=21).sum()/df['volume'].rolling(window=21).sum()*100
        df = df.dropna()
        return df

    def rev_trading(self, df):
        for i in range(0, len(df.close)):
            if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
                self.buy_tim.append(df.index.values[i])
                self.account -= df.close.values[i] * 1
                self.stock += 1
                print(f"[{df.index.values[i]}] 체결완료 - 매수가 : {df.close.values[i]} (원)"
                      f" | 체결 수량 : 1 | 총 {self.stock} 주")
            if df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
                self.sell_tim.append(df.index.values[i])
                if self.stock == 0:
                    continue
                print(f"[{df.index.values[i]}] 체결완료 - 매도가 : {df.close.values[i]} (원)"
                      f" | 체결 수량 : {self.stock} 주")
                self.account += df.close.values[i] * self.stock
                self.stock = 0
        self.profit = self.account + self.stock * df.close.values[len(df.close) - 1] - 1000000
        print('반전 매매 기법 총수익률 : ', self.profit, " (원)")

    def show_II_chart(self, df):
        plt.bar(df.index, df['IIP21'], color='g', label = 'II% 21days')
        plt.grid(linestyle='dotted')
        plt.legend(loc='best')

    def show_rev_trading_chart(self, df):
        plt.plot(self.buy_tim, df.loc[self.buy_tim]['close'], 'r^')
        plt.plot(self.sell_tim, df.loc[self.sell_tim]['close'], 'bv')
        plt.grid(linestyle='dotted')
        plt.legend(loc='best')
        plt.xticks(rotation=45)
