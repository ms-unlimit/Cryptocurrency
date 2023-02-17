import pandas as pd
import finpy_tse as fpy
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)

p = fpy.Get_Price_History(stock='شبریز', start_date='1401-06-01', end_date='1401-11-26',
                           ignore_date=False, adjust_price=False, show_weekday=False, double_date=False)

ri = fpy.Get_RI_History(stock='شبریز', start_date='1401-06-01', end_date='1401-11-26',
    ignore_date=False, show_weekday=False, double_date=False)

avg = 8

ri["Vol_I"] = ri["Vol_Buy_I"] - ri ["Vol_Sell_I"]
ri["Vol_Flw_I"] = ri['Vol_I'].expanding(1).sum()
ri["Vol_Flw_Avg_I"] = ri['Vol_I'].rolling(avg).sum()

ri["Vol_R"] = ri["Vol_Buy_R"] - ri ["Vol_Sell_R"]
ri["Vol_Flw_R"] = ri['Vol_R'].rolling(avg).sum()

ri["Num_R_Buer"] = ri["No_Buy_R"] - ri["No_Sell_R"]
ri["Buer_Flw_R"] = ri['Num_R_Buer'].rolling(avg).sum()

ri["Num_I_Buer"] = ri["No_Buy_I"] - ri["No_Sell_I"]
ri["Buer_Flw_I"] = ri['Num_I_Buer'].rolling(avg).sum()

ax1 = plt.subplot(511)
ax1.plot(p.index.to_list(), p['Final'].to_list())
ax1.title.set_text('price')

ax2 = plt.subplot(512)
ax2.plot(ri.index.to_list(), ri['Vol_Flw_Avg_I'].to_list())
ax2.title.set_text('I avg vol')

# ax3 = plt.subplot(512)
# ax3.plot(ri.index.to_list(), ri['Vol_Flw_I'].to_list())
# ax3.title.set_text('I sum vol')

ax4 = plt.subplot(513)
ax4.plot(ri.index.to_list(), ri["Buer_Flw_I"].to_list())
ax4.title.set_text('I Buy')

ax5 = plt.subplot(514)
ax5.plot(ri.index.to_list(), ri['Vol_Flw_R'].to_list())
ax5.title.set_text('R avg vol')

ax6 = plt.subplot(515)
ax6.plot(ri.index.to_list(), ri["Buer_Flw_R"].to_list())
ax6.title.set_text('R Buy')

plt.show()


# df = fpy.Get_IntradayTrades_History(stock='خودرو', start_date='1400-09-15', end_date='1400-10-15',
#     jalali_date=True, combined_datatime=False, show_progress=True)

# df = fpy.Get_IntradayOB_History(stock='خودرو', start_date='1400-08-01', end_date='1400-08-01',
#     jalali_date=True, combined_datatime=False, show_progress=True)

# df = fpy.Get_Queue_History(stock='خودرو', start_date='1400-09-15', end_date='1400-10-01',
#     show_per_capita=True, show_weekday=False, double_date=False, show_progress=True)

# df = fpy.Get_CWI_History(start_date='1395-01-01', end_date='1400-12-29',
#     ignore_date=False, just_adj_close=False, show_weekday=False, double_date=False)

# df = fpy.Get_INDI_History(start_date='1395-01-01', end_date='1400-12-29',
#     ignore_date=False, just_adj_close=False, show_weekday=False, double_date=False)

# df = fpy.Get_USD_RIAL(start_date='1395-01-01', end_date='1400-12-29',
#     ignore_date=False, show_weekday=False, double_date=False)

print(p.iloc[-1])
