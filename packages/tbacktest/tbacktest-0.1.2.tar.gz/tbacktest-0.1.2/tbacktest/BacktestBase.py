#
# Python Script with Base Class
# for Event-Based Backtesting
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
import numpy as np
import pandas as pd
from pylab import mpl, plt
#import matplotlib.pyplot as plt
import mplfinance as mpf
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

import finlab
from finlab import data





class BacktestBase(object):
    ''' Base class for event-based backtesting of trading strategies.

    Attributes
    ==========
    symbol: str
        TR RIC (financial instrument) to be used
    start: str
        start date for data selection
    end: str
        end date for data selection
    amount: float
        amount to be invested either once or per trade
    ftc: float
        fixed transaction costs per trade (buy or sell)
    ptc: float
        proportional transaction costs per trade (buy or sell)

    Methods
    =======
    get_data:
        retrieves and prepares the base data set
    plot_data:
        plots the closing price for the symbol
    get_date_price:
        returns the date and price for the given bar
    print_balance:
        prints out the current (cash) balance
    print_net_wealth:
        prints out the current net wealth
    place_buy_order:
        places a buy order
    place_sell_order:
        places a sell order
    close_out:
        closes out a long or short position
    '''

    def __init__(self, symbol,start,newest_day,
                 amount=1000000,
                 end=None,
                 newest_price = None,
                 ftc=0.0, ptc=0.0, verbose=True,finlab_password=None
                 ):
        
        finlab.login(finlab_password)
        self.symbol = symbol
        self.start = start
        
        if end is None:
            self.end = newest_day
        else:
            self.end = end
            
        self.initial_amount = amount
        self.amount = amount   #amount指每個時間點帳上資金餘額，注意另外一個net_wealth是amount加上部位市值
        self.ftc = ftc
        self.ptc = ptc
        self.units = 0
        self.position = 0


        self.trades = 0
        self.lost_trades = 0
        self.positive_trades = 0
        self.buy_avg_cost = 0
        self.buy_cost = 0

        self.bt_date =[]          #紀錄歷史回測紀錄中每一天日期
        self.bt_net_wealth = []   #紀錄歷史回測紀錄中，每一天的net_wealth，即 計算每一天net_wealth後記錄到bt_net_wealth中
        self.bt_balance = []
        self.bt_position = []     # 紀錄歷史回測紀錄中的每一天部位狀況
        self.bt_lost_trades = []  #紀錄歷史回測紀錄中每一天當下策略損失已出場次數
        self.bt_balance_ratio = [] # 紀錄現金水位
        

        self.verbose = verbose
        self.newest_day = newest_day
        self.newest_price = newest_price
        self.get_data()

    def get_data(self,data_source=2):

        ''' Retrieves and prepares the data.

        '''

        '''raw = pd.read_csv('http://hilpisch.com/pyalgo_eikon_eod_data.csv',

                          index_col=0, parse_dates=True).dropna()

        '''
        #raw = pd.read_excel(r'C:/Users/80900/Tsung_API/Backtest/bt20241101/db.xlsx',sheet_name= "rawdata", header=0,skiprows=0,usecols="A:F")
        #raw = pd.read_excel(r'C:/Users/tts74/OneDrive/程式相關/Python_AlgoTrading_OREILLY/Backtest/bt20241105/db.xlsx',sheet_name= "rawdata", header=0,skiprows=0,usecols="A:F")

        if data_source == 1 :
            raw = pd.read_excel(r'C:/Users/tts74/OneDrive/程式相關/Python_AlgoTrading_OREILLY/Backtest/db.xlsx',sheet_name= "rawdata", header=0,skiprows=0,usecols="A:F")
            #省略前面4列後，取第0列為表頭
            raw['date']=pd.to_datetime(raw['date'], format='%Y%m%d')
            raw=raw.set_index('date')
            raw = pd.DataFrame(raw[self.symbol].dropna())
            raw = raw.loc[pd.to_datetime(self.start,format='%Y%m%d'):pd.to_datetime(self.end,format='%Y%m%d')]
            raw.rename(columns={self.symbol: 'price'}, inplace=True)
            raw['return'] = np.log(raw / raw.shift(1))
            self.data = raw.dropna()
        else:
            raw = data.get('etl:adj_close')
            raw1= data.get('price:收盤價')
            raw = pd.DataFrame(raw[self.symbol]).dropna()
            raw1 = pd.DataFrame(raw1[self.symbol]).dropna()
            if (self.newest_day is not None) & (self.newest_price is not None) :
                raw.loc[pd.to_datetime(self.newest_day)] = self.newest_price + float((raw[-1:]-raw1[-1:]).values)
                raw1.loc[pd.to_datetime(self.newest_day)] = self.newest_price
                raw = raw.loc[self.start:self.newest_day]
                raw1 = raw1.loc[self.start:self.newest_day]
            else:
                raw = raw.loc[self.start:self.newest_day]
                raw1 = raw1.loc[self.start:self.newest_day]
                
            raw.rename(columns={self.symbol: 'price'}, inplace=True)
            raw1.rename(columns={self.symbol: 'original_price'}, inplace=True)
            raw['return'] = np.log(raw / raw.shift(1))
            
            raw = raw.join(raw1,how='inner')
            self.data = raw

        self.dvd = pd.read_excel(r'dvd_table.xlsx',sheet_name= "dvd",dtype={'ticker': str})

    def plot_data(self, cols=None):
        ''' Plots the closing prices for symbol.
        '''
        if cols is None:
            cols = ['price']
        self.data[cols].plot(figsize=(10, 6), title=self.symbol)

    def get_date_price(self, bar):
        ''' Return date and price for bar.
        '''
        date = self.data.index[bar] #str(self.data.index[bar])[:10]
        original_price = self.data.original_price.iloc[bar]
        return date, original_price

    def print_balance(self, bar):
        ''' Print out current cash balance info. ## blance =cash = amount
        '''
        date, original_price = self.get_date_price(bar)
        print(f'{date} | current balance {self.amount:.0f}')
        
    def print_units(self, bar):
        ''' Print out current units.
        '''
        date, original_price = self.get_date_price(bar)
        print(f'{date} | current units {self.units:.0f}')

    def print_net_wealth(self, bar):
        ''' Print out current cash balance info.
        '''
        date, original_price = self.get_date_price(bar)
        net_wealth = self.units * original_price + self.amount
        print(f'{date} | current net wealth {net_wealth:.0f}')

    
    def record_net_wealth(self, bar):
        ''' Print out current net_wealth,lost_trade times,cash balance info.
        '''
        date, original_price = self.get_date_price(bar)
        net_wealth = round((self.units * original_price + self.amount)/10000,0)
        self.bt_date.append(date)
        self.bt_net_wealth.append(net_wealth)
        self.bt_lost_trades.append(self.lost_trades)
        self.bt_balance_ratio.append( round(self.amount/10000,2)/net_wealth )
        
    

    def record_hist_position(self, bar):
        self.bt_position.append(round(self.units/1000,2))
        self.bt_balance.append(round(self.amount/10000,2))
        
        
    def show_backtest_all_information(self):
        rt = pd.DataFrame({'date':self.bt_date,'net_wealth':self.bt_net_wealth,'position':self.bt_position,'lost_trades':self.bt_lost_trades,'balance':self.bt_balance,'balance_ratio':self.bt_balance_ratio})
        rt.set_index(rt.date,inplace=True,drop=True)
        #rt = 欄位：日期、net_wealth、部位、lost_trades、balance
        return rt

     #當完成策略後，進行策略績效走勢圖輸出
    def plot_backtest(self,):
        df= pd.DataFrame({'date':self.bt_date,'open':self.bt_net_wealth,'high':self.bt_net_wealth,'low':self.bt_net_wealth,'close':self.bt_net_wealth})
        df.set_index(df.date,inplace=True,drop=True)
        bt_plot = mpf.plot(df,
                           title='{} strategy backtesting'.format(self.symbol),
                           type='line',
                           style='yahoo',
                           figsize = (12,6)
                           )
        return bt_plot


    def plot_equity_curve(self):
        """簡單畫出  target-wealth 策略的淨值走勢"""
        plt.figure(0,figsize=(12, 8))
        plt.subplot(3, 1, 1)
        plt.plot(self.bt_date, self.bt_net_wealth)       
        plt.plot(self.bt_date, self.data.target_net_wealth/10000)
        plt.title(f'{self.symbol} Equity Curve')
        plt.xlabel('Date')
        plt.ylabel('Net Wealth')

        plt.subplot(3, 1, 2)
        #plt.title(f'{self.symbol} Cash Balance')
        plt.bar(self.bt_date, self.bt_balance)       
        plt.ylabel('cash balance(10-thousand)')
        
        plt.subplot(3, 1, 3)        
        #plt.title(f'{self.symbol} Position')
        plt.bar(self.bt_date, self.bt_position)
        plt.ylabel('asset position 1000*shares')
        
        
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_target_net_wealth(self):
        """簡單畫出  target-wealth 策略的淨值走勢"""
        plt.figure(0,figsize=(12, 6))
        plt.plot(self.bt_date, self.bt_net_wealth)
        plt.plot(self.bt_date, self.data.target_net_wealth/10000)
        plt.title(f'{self.symbol} Target Net Wealth')
        plt.xlabel('Date')
        plt.ylabel('Target Net Wealth')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_balance_and_position(self):
        """簡單畫出  現金餘額走勢  """

        plt.figure(0,figsize=(12, 8))
        
        plt.subplot(3, 1, 1)
        plt.bar(self.bt_date, self.bt_position)
        plt.title(f'{self.symbol} Holding & Cash Balance ')
        plt.xlabel('Date')
        plt.ylabel('Stock Holding 1000*shares')

        
        plt.subplot(3, 1, 2)        
        plt.bar(self.bt_date, self.bt_balance)       
        plt.ylabel('Cash balance(10k)')
        
        plt.subplot(3, 1, 3)        
        plt.bar(self.bt_date, self.bt_balance_ratio)
        plt.ylabel('Cash balance to NetWealth')
              
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    def plot_balance(self):
        """簡單畫出  現金餘額走勢  """
        plt.figure(figsize=(12, 6))
        plt.bar(self.bt_date, self.bt_balance)
        plt.title(f'{self.symbol} Cash Balance')
        plt.xlabel('date')
        plt.ylabel('cash balance(10-thousand)')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    def plot_position(self):
        """簡單畫出  部位趨勢  """
        plt.figure(figsize=(12, 6))
        plt.bar(self.bt_date, self.bt_position)
        plt.title(f'{self.symbol} Position')
        plt.xlabel('date')
        plt.ylabel('asset position 1000*shares')
        plt.grid(True)
        plt.tight_layout()
        plt.show()       
        
    def place_buy_order(self, bar, units=None, amount=None):
        ''' Place a buy order.
        '''
        date, original_price = self.get_date_price(bar)
        # 如果要使用原始價格(未還原息)，則下單這邊使用的價格就要是原始價格，但策略判斷的價格要使用還息價格
        # 此外帳務面都要注意使用 原始價格
        if units is None:
            units = int(amount / original_price)

        self.amount -= (units * original_price) * (1 + self.ptc) + self.ftc
        self.buy_avg_cost = ((self.buy_avg_cost * self.units) + ( original_price * units )) / ( self.units + units )
        self.buy_cost = original_price
        self.units += units
        self.trades += 1
        if self.verbose:
            print(f'{date} | buying {units} units at {original_price:.2f}')
            self.print_balance(bar)
            self.print_units(bar)
            self.print_net_wealth(bar)

    #如果判斷當下有部位，且是除息是明天，則要試算部位*原始價格，將這筆隔天要除息的資金(假設先從貸款過來的資金)進行再投資
    #如果判斷當下沒有部位，且除息是明天，則不用動作。
    def reinvestment_cash_dividend(self,bar):
        if bar < len(self.data)-1:
            exdvd_next_day = self.dvd[(self.dvd.ticker == self.symbol) & (self.dvd.exdvd_date == self.get_date_price(bar+1)[0])].dvd
        
            if any(exdvd_next_day) :
                new_amount_from_exdvd = int(self.units * exdvd_next_day.iloc[0])
                self.amount += new_amount_from_exdvd
                if self.verbose:
                    print('event trigger: reinvestment because cash dividend')
                self.place_buy_order(bar,amount=new_amount_from_exdvd)





    def place_sell_order(self, bar, units=None, amount=None):
        ''' Place a sell order.
        '''
        date, original_price = self.get_date_price(bar)

        if units is None:
            if(int(amount / original_price) > self.units):
                units = self.units
            else:
                units = int(amount / original_price)

        self.amount += ((units * original_price) * (1 - self.ptc) - self.ftc)
        self.units -= units

        self.trades += 1
        if original_price > self.buy_avg_cost :
            self.positive_trades +=1
            self.lost_trades=0
        elif original_price <= self.buy_avg_cost:
            self.lost_trades+=1

        if self.units == 0:
            self.buy_avg_cost = 0
            self.buy_cost = 0

        if self.verbose:
            print(f'{date} | selling {units} units at {original_price:.2f}')
            self.print_balance(bar)
            self.print_units(bar)
            self.print_net_wealth(bar)
            

    def close_out(self, bar):
        ''' Closing out a long or short position.
        '''
        date, original_price = self.get_date_price(bar)
        self.amount += self.units * original_price
        self.units = 0
        self.trades += 1
        if self.verbose:
            print(f'{date} | inventory {self.units} units at {original_price:.2f}')
            print('=' * 55)
        print('Final balance   [$] {:.0f}'.format(self.amount))
        perf = ((self.amount - self.initial_amount) /
                self.initial_amount * 100)
        print('Net Performance [%] {:.0f}'.format(perf))
        print('Trades Executed [#] {}'.format(self.trades))
        print('=' * 55)
        self.final_perf = perf




if __name__ == '__main__':
    bb = BacktestBase('AAPL.O', '2010-1-1', '2019-12-31', 10000)
    print(bb.data.info())
    print(bb.data.tail())
    bb.plot_data()
    plt.savefig('../../images/ch06/backtestbaseplot.png')
