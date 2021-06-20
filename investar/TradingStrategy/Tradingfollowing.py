from Investar.BollingerBand import BollingerBand
import matplotlib.pyplot as plt

class TradingFollowing():

    def __init__(self, company, start_date):
        bB = BollingerBand()
        self.df = bB.get_bollinger_band(company, start_date)
        self.buy_tim = []
        self.sell_tim = []
        self.account = 1000000
        self.stock = 0
        self.profit = 0

    def calc_mfi(self):
        df = self.df
        df['TP'] = (df['high'] + df['low'] + df['close']) / 3
        df['PMF'] = 0
        df['NMF'] = 0
        for i in range(len(df.close)-1):
            if df.TP.values[i] < df.TP.values[i+1]:
                df.PMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
                df.NMF.values[i+1] = 0
            if df.TP.values[i] > df.TP.values[i+1]:
                df.NMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
                df.PMF.values[i+1] = 0
        df['MFR'] = df.PMF.rolling(window=14).sum()/df.NMF.rolling(window=14).sum()
        df['MFI'] = 100 - 100/(1+df['MFR'])
        df = df[13:]
        return df

    def trading_follow(self, df):
        for i in range(len(df.close)):
            if df.PB.values[i] > 0.8 and df.MFI.values[i] > 80:
                self.buy_tim.append(df.index.values[i])
                self.account -= df.close.values[i] * 1
                self.stock += 1
                print(f"[{df.index.values[i]}] 체결완료 - 매수가 : {df.close.values[i]} (원)"
                      f" | 체결 수량 : 1 | 총 {self.stock} 주")
            if df.PB.values[i] < 0.2 and df.MFI.values[i] < 20:
                self.sell_tim.append(df.date.values[i])
                if self.stock == 0:
                    continue
                print(f"[{df.index.values[i]}] 체결완료 - 매도가 : {df.close.values[i]} (원)"
                      f" | 체결 수량 : {self.stock} 주")
                self.account += df.close.values[i]*self.stock
                self.stock = 0
        self.profit = self.account + self.stock * df.close.values[len(df.close)-1] - 1000000
        print('추세 추종 매매 기법 총수익률 : ', self.profit, " (원)")

    def show_MFI_chart(self, df):
        plt.plot(df.index, df['MFI'], 'g--', label='MFI')
        plt.grid(linestyle='dotted')
        plt.legend(loc='best')
        plt.xticks(rotation=45)

    def show_trading_follow(self, df):
        plt.plot(self.buy_tim, df.loc[self.buy_tim]['close'], 'r^')
        plt.plot(self.sell_tim, df.loc[self.sell_tim]['close'], 'bv')
        plt.grid(linestyle='dotted')
        plt.legend(loc='best')
        plt.xticks(rotation=45)







