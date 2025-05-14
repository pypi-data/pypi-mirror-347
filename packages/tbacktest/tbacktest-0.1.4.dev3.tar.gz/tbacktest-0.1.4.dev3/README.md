## 套件簡介

這是一個自製的 Python 套件，實作了 backtesting 功能。
參考OREILLY的Python演算法交易該書本中所描述，以事件觸發導向的交易策略回測。
此回測方法是這麼多種回測方法中，作者認為最為細緻且彈性與變化度最高的方法。


## 安裝方式

```bash
pip install tbacktest
```

## 指令範例

動能突破策略，以ETF:00713為例

```bash
clo713 = BacktestLongOnly(symbol='00713', start='20171001', newest_day='20250512',amount=1000000,
                          datasource='finlab',
                          finlab_password='finlab_api_token')
#將LongOnly類別實體化出clo713

clo713.run_break_high_strategy(Hday=10, Lday=10,SMA1=5,SMA2=10)
#執行該類別下的方法，及突破進場買進ETF，跌破平倉出場ETF。

clo713.plot_backtest()  
#將策略結果圖示化
clo713.plot_data()
#將原本資料畫出來

clo713.show_backtest_all_information()
#顯示所有回測結果時間序列
```

