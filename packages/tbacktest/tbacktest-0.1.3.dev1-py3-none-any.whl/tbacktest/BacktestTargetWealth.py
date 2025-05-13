# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 19:13:39 2025

@author: tts74
"""
from .BacktestBase import BacktestBase
import pandas as pd

class BacktestTargetWealth(BacktestBase):
    def __init__(self, symbol,start,newest_day,amount,
                 end=None,
                 contribution = 10000, 
                 expected_annual_return = 0.09,
                 threshold = 0.025,   # 新增：允許偏離多少才交易
                 dynamic_ret=False,
                 ftc=0.0, ptc=0.008, verbose=True,newest_price=None,datasource='excel',finlab_password=None):
        
        
        super().__init__(symbol,start,newest_day,
                         amount,end,
                         newest_price,
                         ftc, ptc, verbose,
                         datasource,
                         finlab_password,
                         )
        ### 把 father類別放入，可以直接將些屬性方法直接引用進入 ex self.initial_amount
        
        # 每次注入金額
        self.contribution = contribution
        
        # x% 門檻
        self.threshold = threshold  
        
        
        #是否啟用動態報酬率方法
        self.dynamic_ret = dynamic_ret
        
        if self.dynamic_ret is False:
            #年化期望報酬率
            self.expected_annual_return = expected_annual_return
            #計算每日報酬率（簡單離散化）
            self.r_daily = (1 + expected_annual_return) ** (1/252) - 1
        

    def prepare_target_series(self):
        """ 
        預先計算每個交易日的目標淨值序列，並且每週第二個交易日注入 contribution。
        """
        dates = self.data.index
        
        if self.dynamic_ret is False:
            
            #    先算出「動態年化報酬率」序列（以 60 日累積報酬外推年化）
            #    exp_ann_ret(today) = (price_today / price_60d_ago)^(252/60) - 1
            
            roll = 120
            self.data['exp_ann_ret'] = (self.data['price'] / self.data['price'].shift(roll))**(252/roll) - 1
            # 再由 exp_ann_ret 轉成當日的日化報酬率
            self.data['r_daily_dyn'] = (1 + self.data['exp_ann_ret']) ** (1/252) - 1
            self.data['r_daily_dyn'].fillna(0, inplace=True)
            
            '''
            重點說明：
            exp_ann_ret：用過去 60 天的價格變動外推年化報酬。
            r_daily_dyn：再由每筆年化報酬換算成當日報酬率。
            prepare_target_series 中，每天都採用最新的 r_daily_dyn 讓基準曲線隨市況「彈性」調整。
            後續在 run_target_wealth_strategy 中，就直接沿用 target_net_wealth，不需要再變動其他邏輯。
            你也可以改用其他訊號（像是因子模型、宏觀指標等）來產生更複雜的 exp_ann_ret 序列。
            '''
        
        
        # 2. 找每週第二交易日 ####################################
        # 建立 DataFrame 幫助找出每週第二個交易日
        df_dates = pd.DataFrame(index=dates)
        df_dates['year'] = df_dates.index.isocalendar().year
        df_dates['week'] = df_dates.index.isocalendar().week

        # 找出每 (year, week) 群組裡的第二個交易日
        # 如果該週交易日數 < 2，則不注資
        second_days = (
            df_dates
            .groupby(['year', 'week'])
            .apply(lambda grp: grp.index.sort_values()[1] if len(grp) >= 2 else None)
            #.nth(1)
            .dropna()
            .tolist()
        )
        self.second_days = set(second_days)
        
        # 3. 生成 target_net_wealth 序列 ########################
        target = self.initial_amount
        targets = []
        
        
        if self.dynamic_ret is False:
            # 對每一天計算：若為週第二交易日，先注資；再按日化期望報酬率成長
            
            for today in dates:
                if today in second_days:
                    target += self.contribution
                target *= (1 + self.r_daily)
                targets.append(target)
        else:
            for i, today in enumerate(dates):
                
                if today in self.second_days:
                    target += self.contribution
                # 用當日動態日報酬率成長
                rd = self.data['r_daily_dyn'].iloc[i]
                target *= (1 + rd)
                targets.append(target)
            
        self.data['target_net_wealth'] = pd.Series(targets, index=dates)
        

    def run_target_wealth_strategy(self,buy_adj_ratio=0.3,sell_adj_ratio=0.15,
                                   new_money_buy=True,
                                   Target_For_Asset_NetWealth = "NetWealth"):
        """執行「偏離 ±threshold 才交易」的回測。"""
        
        ######## 這裡要把上面判斷每週第二個交易日的contribution注資到amount中，這樣實際部位才有足夠的錢支應
        ##### 目前只有在 place_buy or place_sell的method中才有加減amount效果，應該要設定一個新的method在特定bar中可以加減amount
        # 重置
        self.units = 0; self.position = 0
        self.amount = self.initial_amount
        self.trades = 0
        self.bt_date = []; self.bt_net_wealth = [] ; self.bt_balance = [] ;  self.bt_balance_ratio = []
        self.bt_position = []; self.bt_lost_trades = []
        self.final_units=0;self.final_balance=0;self.final_stock_marketvalue=0;self.fianl_net_wealth=0
        
        # 1) 計算 target_net_wealth 和 second_days
        self.prepare_target_series()

        # 2) **一開盤就全倉買進所有本金**
        #    bar=0 代表第一個交易日
        self.place_buy_order(bar=0, amount=self.amount)
        self.position = 1
        # 記錄第一筆淨值
        self.record_net_wealth(0)
        self.record_hist_position(0)

        # 3) 從第二根 K 線開始，依 ±threshold 調整差額

        for bar, today in enumerate(self.data.index[1:], start=1):
            original_price  = self.data.original_price.iloc[bar]
            target = self.data.target_net_wealth.iloc[bar]
            
            if Target_For_Asset_NetWealth == "NetWealth" :
                actual = self.units * original_price  + self.amount
            elif Target_For_Asset_NetWealth == "Asset" :
                actual = self.units * original_price
            
            # 先不管今天是否為注資日，先判斷有沒有需要dvd reinvest
            self.reinvestment_cash_dividend(bar)
            
            
            # 若今天是注資日，也把 contribution 加到 self.amount
            if today in self.second_days:
                self.amount += self.contribution
                
                if new_money_buy == True:
                    # 指定每次拿到新的資金就直接將注資金額買入股票
                    self.place_buy_order(bar,amount=self.contribution)
                    
                    if Target_For_Asset_NetWealth == "NetWealth" :
                        actual = self.units * original_price  + self.amount
                    elif Target_For_Asset_NetWealth == "Asset" :
                        actual = self.units * original_price
                else:
                    
                    if Target_For_Asset_NetWealth == "NetWealth" :
                        actual += self.contribution  # 更新 actual 以便當日交易
                    elif Target_For_Asset_NetWealth == "Asset" :
                        actual += 0
                    
                
                # 計算偏離率
                diff_pct = (actual - target) / target

                # 若偏離超過門檻，才進場或出場
                if diff_pct <= -self.threshold and self.amount > 0:
                    # 實際低於目標超過 threshold → 買入差額
                    buy_amt = min(self.amount,round( (target - actual) * buy_adj_ratio ,0) )
                    self.place_buy_order(bar, amount=buy_amt)
                    self.position = 1
    
                elif diff_pct >= self.threshold and self.units > 0:
                    # 實際高於目標超過 threshold → 賣出超額
                    sell_amt = round( (actual - target) * sell_adj_ratio ,0 )
                    sell_units = min(round(self.units/2,0),int(sell_amt/original_price))
                    #這裡改寫成明確的units 且永遠只砍最多原本庫存的一半部位
                    self.place_sell_order(bar, units=sell_units)
                    if self.units == 0:
                        self.position = 0

            # 不論是否交易，都要記錄當天狀態
            self.record_net_wealth(bar)
            self.record_hist_position(bar)

        # 完成後平倉並印出績效
        self.final_units=round(self.units/1000,2)
        self.final_balance = round(self.amount/10000,2)
        self.final_stock_marketvalue = round((self.final_units * original_price )/10,2)
        self.fianl_net_wealth = round((self.units * original_price + self.amount)/10000,2)
        self.close_out(bar)


