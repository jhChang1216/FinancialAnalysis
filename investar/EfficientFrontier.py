import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Investar.MarketDB import MarketDB

class EfficientFrontier:

    def __init__(self, stock_list, start_date, end_date):
        self.daily_ret = []
        self.annual_ret = []
        self.daily_cov = []
        self.annual_cov = []
        self.stocks = pd.DataFrame()

        self.port_ret = []
        self.port_risk = []
        self.port_weight = []
        self.sharpe_ratio = []

        self.calc_indict(stock_list, start_date, end_date)

    def calc_indict(self, stock_list, start_date, end_date):
        mk = MarketDB()

        for s in stock_list:
            self.stocks[s] = mk.get_daily_price(s, start_date, end_date)['close']

        self.daily_ret = self.stocks.pct_change()
        self.annual_ret = self.daily_ret.mean()*252
        self.daily_cov = self.daily_ret.cov()
        self.annual_cov = self.daily_cov * 252

        print(self.daily_ret)
        print(self.annual_ret)
        print(self.daily_cov)
        print(self.annual_cov)
        return

    def monte_carlo_sim(self, stock_list):
        for _ in range(20000):
            weights = np.random.random(len(stock_list))
            total_weight = np.sum(weights)
            weights /= total_weight

            returns = np.dot(weights, self.annual_ret)
            risk = np.sqrt(np.dot(weights.T, np.dot(self.annual_cov, weights)))

            self.port_ret.append(returns)
            self.port_risk.append(risk)
            self.port_weight.append(weights)
            self.sharpe_ratio.append(returns/risk)

        portfolio = {'Returns' : self.port_ret, 'Risk' : self.port_risk, 'Sharpe':self.sharpe_ratio}
        for i, s in enumerate(stock_list):
            portfolio[s] = [weight[i] for weight in self.port_weight]

        portfolio = pd.DataFrame(portfolio)
        max_sharpe = portfolio.loc[portfolio['Sharpe'] == portfolio['Sharpe'].max()]
        min_risk = portfolio.loc[portfolio['Risk'] == portfolio['Risk'].min()]

        print(portfolio)
        print(max_sharpe)
        print(min_risk)

        portfolio.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap = 'viridis',edgecolors='k', grid=True)
        plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r', marker='X', s=200)
        plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r', marker='*', s=300)
        plt.title("Efficient Frontier")
        plt.xlabel('Risk')
        plt.ylabel('Expected Returns')
        plt.show()
        return portfolio










