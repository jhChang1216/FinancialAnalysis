import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from matplotlib import pyplot as plt
import mplfinance as mpf
from Investar.DBUpdater import DBUpdater
from Investar.DisplayChart import displayChart
from Investar.EfficientFrontier import EfficientFrontier
from Investar.BollingerBand import BollingerBand
from Investar.TradingStrategy.Tradingfollowing import TradingFollowing
from Investar.TradingStrategy.Reversals import ReversalsTrading
from Investar.TradingStrategy.TripleScreen import TripleScreen



if __name__ == '__main__':

    print("START")
    dbu = DBUpdater()
    dbu.execute_daily()

    company = "현대자동차"
    start_date = '2018-06-01'

    bB = BollingerBand()
    df = bB.get_bollinger_band(company, start_date)

    tf = TradingFollowing(company, start_date)
    df = tf.calc_mfi()
    tf.trading_follow(df)

    rt = ReversalsTrading(company, start_date)
    df = rt.calc_II(df)
    rt.rev_trading(df)

    plt.subplot(3, 1, 1)
    bB.show_bollinger_chart(df,company)
    rt.show_rev_trading_chart(df)
    plt.subplot(3, 1, 2)
    bB.show_pb_chart(df, 100)
    tf.show_MFI_chart(df)
    plt.subplot(3, 1, 3)
    rt.show_II_chart(df)
    plt.tight_layout()
    plt.show()

    company = '이마트'
    start_date = '2019-08-01'

    tw = TripleScreen(company, start_date)
    tw.get_market_tide()
    p1 = plt.subplot(3,1,1)
    tw.show_candle_chart(p1)
    p2 = plt.subplot(3,1,2)
    tw.show_macd_chart(p2)
    tw.get_market_wave()
    p3 = plt.subplot(3,1,3)
    tw.show_stochastic_chart(p3)
    plt.show()

    tw.sim_trade()
