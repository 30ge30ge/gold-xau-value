# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 09:04:35 2019

@author: Administrator
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_finance as mpf
import datetime
from matplotlib.pylab import date2num
import talib
import statsmodels.api as sm
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus']=False
df = pd.read_csv("F:/数据分析/MT4/XAGUSD1.29.csv",engine='python',sep=",")
df["时间"]=df["TIME"]+" "+df["time"]
df=df[["时间","收盘价"]]
Df=pd.read_csv("F:/数据分析/MT4/XAUUSD1.29.csv",engine='python',sep=",")
Df["时间"]=Df["TIME"]+" "+Df["time"]
Df=Df[["时间","收盘价"]]
df_new=pd.merge(df,Df,on="时间")
df_new.rename(columns={"收盘价_x":"xagusd", "收盘价_y":"xauusd"}, inplace = True)
df_new["时间"]=pd.to_datetime(df_new["时间"])
df_new.set_index("时间", inplace=True)
df_new["50xagusd"]=df_new["xagusd"]*50
df_new["价差"]=df_new["xauusd"]-df_new["50xagusd"]
print(df_new)

A=df_new["2019-01-25":"2019-01-25"]
B=df_new["2019-01-27":]
C=df_new["2019-01-01":"2019-01-28"]
print(A)

spread=A["价差"].tolist()
avg=np.mean(spread)
print("价差均值为:",avg)
up=avg+np.std(spread)
print("上轨为",up)
down=avg-np.std(spread)
print("下轨为",down)
print("价差最大数:",np.max(spread))
print("价差中位数:",np.median(spread))
print("价差最小数:",np.min(spread))
print("标准差为：",np.std(spread))

fig,ax=plt.subplots(figsize=(16,8))
plt.title("价差走势图")
plt.plot(C["价差"])
plt.xticks(rotation=75)
avg_5 = talib.EMA(C["价差"], timeperiod=24)
plt.plot(avg_5,color="r")
plt.ylabel("价差值")
plt.show()
print(avg_5)
#以下为做空XAG做多XAU
close_down=down+2.3
df_short=B.loc[lambda B: B.价差 <down, :]
df_long=B.loc[lambda B: B.价差 >close_down, :]
print("多XAU,空XAG")
print(df_short.head(5))
print("平仓点位")
print(df_long.head(1))
E=df_short.head(5).append(df_long.head(1))
print(E)

#以下为做空XAU，做多XAG
CLOSE=up-2.3
XAU_short=B.loc[lambda B: B.价差 >up, :]
XAU_CLOSE=B.loc[lambda B: B.价差 <CLOSE, :]
print("做空xau做多xag的订单为：")
print(XAU_short.head(5))
print(XAU_CLOSE)
#线性相关检查
X=df_new["xauusd"]
Y=df_new["xagusd"] 
model=sm.OLS(Y,X)
result=model.fit()
print(result.summary())
print("回归系数为：",result.params)
print("R2:",result.rsquared)
print("R2无限接近与1,线性相关显著")
y_fitted=result.fittedvalues
fig,ax=plt.subplots(figsize=(12,4))
plt.title("xau-xag跨品种线性相关图")
ax.plot(X,Y,"o",label="data")
ax.plot(X,y_fitted,"r--.",label="OLS")
ax.legend(loc="best")
plt.show()






