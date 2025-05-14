#
# Python Script with Long Only Class
# for Event-based Backtesting
#
# Python for Algorithmic Trading
# (c) Dr. Yves J. Hilpisch
# The Python Quants GmbH
#
from .BacktestBase import BacktestBase
import numpy as np
import pandas as pd
# 

class BacktestLongOnly(BacktestBase):
    def __init__(self, symbol,start,newest_day,amount,
                 end=None,
                 newest_price=None,
                 ftc=0.0, 
                 ptc=0.0008,
                 verbose=True,
                 datasource='excel',
                 finlab_password=None):
        
        
        super().__init__(symbol,start,newest_day,
                         amount,end,
                         newest_price,
                         ftc, ptc, verbose,
                         datasource,
                         finlab_password,
                         )
        
    def run_sma_strategy(self, SMA1, SMA2):
        ''' Backtesting a SMA-based strategy.

        Parameters
        ==========
        SMA1, SMA2: int
            shorter and longer term simple moving average (in days)
        '''
        msg = f'\n\nRunning SMA strategy | SMA1={SMA1} & SMA2={SMA2}'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)
        self.units = 0
        self.position = 0  # initial neutral position
        self.trades = 0  # no trades yet

        self.positive_trades=0
        self.lost_trades = 0

        self.bt_date =[]
        self.bt_net_wealth = []
        self.bt_lost_trades = []
        self.bt_position = []

        self.buy_cost=0
        self.buy_avg_cost=0
        self.amount = self.initial_amount  # reset initial capital
        self.data['SMA1'] = self.data['price'].rolling(SMA1).mean()
        self.data['SMA2'] = self.data['price'].rolling(SMA2).mean()

        for bar in range(SMA2, len(self.data)):
            if self.position == 0:
                if self.data['SMA1'].iloc[bar] > self.data['SMA2'].iloc[bar]:
                    self.place_buy_order(bar, amount=self.amount)
                    self.position = 1  # long position
            elif self.position == 1:
                if self.data['SMA1'].iloc[bar] < self.data['SMA2'].iloc[bar]:
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0  # market neutral
            self.record_net_wealth(bar)
            self.record_hist_position(bar)
        self.final_units=self.units
        self.close_out(bar)

    def run_momentum_strategy(self, momentum):
        ''' Backtesting a momentum-based strategy.

        Parameters
        ==========
        momentum: int
            number of days for mean return calculation

        '''
        msg = f'\n\nRunning momentum strategy | {momentum} days'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)
        self.units = 0
        self.position = 0  # initial neutral position
        self.trades = 0  # no trades yet

        self.positive_trades=0
        self.lost_trades = 0

        self.bt_date =[]
        self.bt_net_wealth = []
        self.bt_lost_trades = []
        self.bt_position = []

        self.buy_cost=0
        self.buy_avg_cost=0
        self.amount = self.initial_amount  # reset initial capital
        self.data['momentum'] = self.data['return'].rolling(momentum).mean()
        for bar in range(momentum, len(self.data)):
            if self.position == 0:
                if self.data['momentum'].iloc[bar] > 0:
                    self.place_buy_order(bar, amount=self.amount)
                    self.position = 1  # long position
            elif self.position == 1:
                if self.data['momentum'].iloc[bar] < 0:
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0  # market neutral

            self.record_net_wealth(bar)
            self.record_hist_position(bar)

        self.final_units=self.units
        self.close_out(bar)

    def run_mean_reversion_strategy(self, SMA, threshold):
        ''' Backtesting a mean reversion-based strategy.

        Parameters
        ==========
        SMA: int
            simple moving average in days
        threshold: float
            absolute value for deviation-based signal relative to SMA
        '''
        msg = f'\n\nRunning mean reversion strategy | '
        msg += f'SMA={SMA} & thr={threshold}'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)
        self.units = 0
        self.position = 0  # initial neutral position
        self.trades = 0  # no trades yet

        self.positive_trades=0
        self.lost_trades = 0

        self.bt_date =[]
        self.bt_net_wealth = []
        self.bt_lost_trades = []
        self.bt_position = []

        self.buy_cost=0
        self.buy_avg_cost=0
        self.amount = self.initial_amount

        self.data['SMA'] = self.data['price'].rolling(SMA).mean()

        for bar in range(SMA, len(self.data)):
            if self.position == 0:
                if (self.data['price'].iloc[bar] <
                        self.data['SMA'].iloc[bar] - threshold):
                    self.place_buy_order(bar, amount=self.amount)
                    self.position = 1
            elif self.position == 1:
                if self.data['price'].iloc[bar] >= self.data['SMA'].iloc[bar]:
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0

            self.record_net_wealth(bar)
            self.record_hist_position(bar)

        self.final_units=self.units
        self.close_out(bar)


    def run_break_high_strategy(self, Hday,Lday,SMA1=55,SMA2=252):
        ''' Backtesting a breaking the High price in the past N day strategy.
        Parameters
        ==========
        Hday: int
            過去 N Days 的收盤最高價
        Hday: int
            過去 N Days 的收盤最低價
        SMA1, SMA2: int

        最新收盤價 >= 過去 N Days 的收盤最高價則進場做多。
        最新收盤價 <= 過去 N Days 的收盤最低價則出場
        若短均SMA < 長均SMA 則出場
        '''
        msg = f'\n\nRunning Hday break up to buy | Lday break down to sell  &SMA strategy | SMA1={SMA1} & SMA2={SMA2}'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)
        self.units = 0
        self.position = 0  # initial neutral position
        self.trades = 0  # no trades yet

        self.positive_trades=0
        self.lost_trades = 0

        self.bt_date =[]
        self.bt_net_wealth = []
        self.bt_lost_trades = []
        self.bt_position = []
        self.bt_balance = []
        self.bt_balance_ratio = []

        self.buy_cost=0
        self.buy_avg_cost=0
        self.amount = self.initial_amount  # reset initial capital
        
        self.data['Hday'] = self.data['price'].rolling(Hday).max()
        self.data['Lday'] = self.data['price'].rolling(Lday).min()
        self.data['SMA1'] = self.data['price'].rolling(SMA1).mean()
        self.data['SMA2'] = self.data['price'].rolling(SMA2).mean()


        for bar in range(Hday, len(self.data)):
            if self.position == 0:
                if self.data['price'].iloc[bar] >= self.data['Hday'].iloc[bar]:
                    self.place_buy_order(bar, amount=self.amount)
                    self.reinvestment_cash_dividend(bar) #沒有部位也有可能剛好遇到除息前觸發買進訊號，所以需要立刻再投資
                    self.position = 1  # long position
            elif self.position == 1:
                self.reinvestment_cash_dividend(bar)
                #只要有部位，就要持續監控是否遇到除息事件
                if (self.data['price'].iloc[bar] <= self.data['Lday'].iloc[bar] or
                       self.data['SMA1'].iloc[bar] < self.data['SMA2'].iloc[bar]):
                    #兩個出場條件，任一條件滿足即可
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0  # market neutral
               

            self.record_net_wealth(bar)
            self.record_hist_position(bar)

        self.final_units=self.units
        self.close_out(bar)

    def run_buy_butt(self,SMA,threshold,main_object,consecutive_lost=2):
        ''' Backtesting a mean reversion-based strategy.

        Parameters
        ==========
        SMA: int
            simple moving average in days
        threshold: float
            absolute value for deviation-based signal relative to SMA
        '''
        msg = f'\n\nRunning mean reversion strategy | '
        msg += f'SMA={SMA} & thr={threshold}'
        msg += f'\nfixed costs {self.ftc} | '
        msg += f'proportional costs {self.ptc}'
        print(msg)
        print('=' * 55)
        self.units = 0
        self.position = 0  # initial neutral position
        self.trades = 0  # no trades yet

        self.positive_trades=0
        self.lost_trades = 0

        self.bt_date =[]
        self.bt_net_wealth = []
        self.bt_lost_trades = []
        self.bt_position = []

        self.buy_cost=0
        self.buy_avg_cost=0
        self.amount = self.initial_amount

        self.data['SMA'] = self.data['price'].rolling(SMA).mean()


        for bar in range(SMA, len(self.data)):
            if self.position == 0:
                if ( main_object.show_backtest_all_information().loc[self.data.index[bar]].position == 0 and main_object.show_backtest_all_information().loc[self.data.index[bar]].lost_trades>=consecutive_lost and self.data['price'].iloc[bar] < (self.data['SMA'].iloc[bar] - self.data['SMA'].iloc[bar]*2*threshold)):
                    self.place_buy_order(bar, amount=self.amount)
                    self.position = 1
            elif self.position == 1:
                if self.data['price'].iloc[bar] >= (self.data['SMA'].iloc[bar]+ self.data['SMA'].iloc[bar]*threshold):
                    self.place_sell_order(bar, units=self.units)
                    self.position = 0

            self.record_net_wealth(bar)
            self.record_hist_position(bar)

        self.final_units=self.units
        self.close_out(bar)

    def run_all_strategy(self):

        self.df_aum = pd.DataFrame()
        self.df_position = pd.DataFrame()

        # ST1
        self.run_sma_strategy(10,20)
        df_aum=pd.DataFrame(self.show_backtest_all_information()['net_wealth'])
        df_aum.rename(columns={'net_wealth': self.symbol+'_sma'}, inplace=True)

        df_position = pd.DataFrame(self.show_backtest_all_information()['position'])
        df_position.rename(columns={'position': self.symbol+'_sma'}, inplace=True)

        #ST2
        self.run_momentum_strategy(55)
        df_aum= pd.merge(df_aum,self.show_backtest_all_information()['net_wealth'],how='left',on='date')
        df_aum.rename(columns={'net_wealth': self.symbol+'_momentum'}, inplace=True)

        df_position= pd.merge(df_position,self.show_backtest_all_information()['position'],how='left',on='date')
        df_position.rename(columns={'position': self.symbol+'_momentum'}, inplace=True)

        #ST3
        self.run_break_high_strategy(Hday=10, Lday=10,newest_day='20250421',newest_price = 54.2,SMA1=5,SMA2=10)
        df_aum= pd.merge(df_aum,self.show_backtest_all_information()['net_wealth'],how='left',on='date')
        df_aum.rename(columns={'net_wealth': self.symbol+'_break'}, inplace=True)

        df_position= pd.merge(df_position,self.show_backtest_all_information()['position'],how='left',on='date')
        df_position.rename(columns={'position': self.symbol+'_break'}, inplace=True)

        self.df_aum = df_aum
        self.df_position = df_position

        return df_aum,df_position



if __name__ == '__main__':
    def run_strategies():
        lobt.run_sma_strategy(42, 252)
        lobt.run_momentum_strategy(60)
        lobt.run_mean_reversion_strategy(50, 5)
    lobt = BacktestLongOnly('AAPL.O', '2010-1-1', '2019-12-31', 10000,
                            verbose=False)
    run_strategies()
    # transaction costs: 10 USD fix, 1% variable
    lobt = BacktestLongOnly('AAPL.O', '2010-1-1', '2019-12-31',
                            10000, 10.0, 0.01, False)
    run_strategies()
