#雙均線策略
from operator import itemgetter
import random
import matplotlib.pyplot as plt
import numpy as np
import queue
import pandas as pd
import requests as r
import pandas as pd
import random,time
import threading
from datetime import datetime, date
from io import StringIO
import plotly.express as pe
import plotly.graph_objects as go
from multiprocessing import Pool
from AIFT_plotly_finance import *


def TwoMA(data , period , small_MA_period , long_MA_period , init_money , invest_percent , print_graph = False) :

    # 確保 Long MA  > Small MA
    if long_MA_period < small_MA_period:
        long_MA_period , small_MA_period = small_MA_period , long_MA_period        

    money = init_money
    stock = 0
    assets = init_money
    

    long_MA_sum = 0
    long_MA_days = 0
    long_MA_index = 0
    small_MA_sum = 0
    small_MA_days = 0
    small_MA_index = 0
    
    last_small_MA = 0
    last_long_MA = 0



    if print_graph:
        # history = pd.DataFrame(columns = ["Date" , "Money" , "Stock"])
        # history =  pd.concat([history , pd.Series(["init" , init_money , 0] , index =  ["Date" , "Money" , "Stock"]).to_frame().T])
        # MA_history = pd.DataFrame(columns = ["Date" , "Small MA" , "Long MA"])
        
        history = pd.DataFrame(columns = ["Money" , "Stock"])
        history =  pd.concat([history , pd.Series([init_money , 0] , index =  ["Money" , "Stock"]).to_frame().T])
        
        MA_history = pd.DataFrame(columns = ["Small MA" , "Long MA"])
        MA_history = pd.concat([MA_history , pd.Series([0 , 0 ] , index =  ["Small MA" , "Long MA"]).to_frame().T])

        
    

    for index , row in data.iterrows():
        
        
        # 加上昨天的收盤價
        # print(index)
        if index == 0:
            continue

        small_MA_sum += data.loc[index - 1 , "Close"]
        long_MA_sum += data.loc[index - 1 , "Close"]
       

        # print(small_MA_index , " " , long_MA_index)

        # 如果未滿MA天數就不推動index
        if small_MA_days == small_MA_period:
            small_MA_sum -= data.loc[small_MA_index , "Close"]
            small_MA_index += 1
        else:
            small_MA_days += 1

        if long_MA_days == long_MA_period:
            long_MA_sum -= data.loc[long_MA_index , "Close"]
            long_MA_index += 1
        else:
            long_MA_days += 1

        # 算出昨天的MA
        current_small_MA = small_MA_sum / (small_MA_days)
        current_long_MA = long_MA_sum / (long_MA_days)

        # print(current_small_MA , " " , current_long_MA)
        # print(small_MA_sum , " " , long_MA_sum , " " , long_MA_period)

        # 短MA由上穿越長MA做空
        if last_small_MA > last_long_MA and current_small_MA < current_long_MA:
            # money += stock * invest_percent * row["Close"]
            money += sell_stock(stock * invest_percent , row["Close"])
            stock *= (1.0 - invest_percent)
        # 短MA由下穿越長MA做多
        elif last_long_MA > last_small_MA and current_long_MA < current_small_MA:
            # stock += money * invest_percent / row["Close"] 
            stock += buy_stock(money * invest_percent , row["Close"])
            money *= (1.0 - invest_percent)

        # print(money, " " ,stock)

        # 存下昨天的MA 下次for = 前天的MA
        last_small_MA = current_small_MA
        last_long_MA = current_long_MA
        assets = money + stock * row["Close"]

        

        if print_graph:
            
            # history =  pd.concat([history , pd.Series([row["Date"] , money + stock * row["Close"], stock * row["Close"]] , index =  ["Date" , "Money" , "Stock"]).to_frame().T])
            history =  pd.concat([history , pd.Series([money + stock * row["Close"], stock * row["Close"]] , index =  ["Money" , "Stock"]).to_frame().T])
            MA_history = pd.concat([MA_history , pd.Series([current_small_MA , current_long_MA] , index =  ["Small MA" , "Long MA"]).to_frame().T] )
            # MA_history = pd.concat([MA_history , pd.Series([row["Date"] , current_small_MA , current_long_MA] , index =  ["Date" , "Small MA" , "Long MA"]).to_frame().T]  )
            
            # print(history)

    if print_graph:
        
        MA_history =  MA_history.reset_index(drop = True)
        history =  history.reset_index(drop = True)
        # print (Boolinger_history)
        # print (history)

        all_data = pd.concat([data , MA_history  , history] , axis = 1)
        # all_data = pd.concat([all_data , history] , axis = 1)
        # print(all_data)
        draw_Candlestick(all_data , draw_TwoMA = True)
        draw_accumulated_capital(all_data)



    # print(time.perf_counter() - t )
    return (((assets - init_money) / init_money + 1 ) ** (1 / period) - 1 ) * 100
    # return (assets - init_money) / init_money * 100
    
#解碼
def TwoMA_decode(chromosome):
    #染色體長度 雙均線各 8 bit (0~255) 投資比例 7 bit (0~127)

    long_MA = int(chromosome[8:16], 2) + 1
    small_MA = int(chromosome[0:8], 2) + 1
    invest_percent = 100 / 127 * int(chromosome[16:], 2) / 100

    return small_MA , long_MA ,invest_percent

def TwoMA_Fitness_Process(chromosome , training_data , period , init_money):


    small_MA , long_MA , invest_percent = TwoMA_decode(chromosome)
    IRR = TwoMA(training_data , period , small_MA , long_MA , init_money , invest_percent)
    return IRR

def TwoMA_validate ( best_chromosome , val_data , periods , init_money):
    long_MA = int(best_chromosome[8:16], 2) + 1
    small_MA = int(best_chromosome[0:8], 2) + 1
    invest_percent = 100 / 127 * int(best_chromosome[16:], 2) / 100
    print("long_MA: ", long_MA, "\nsmall_MA: ", small_MA , "\ninvest_percent: ",invest_percent)
    IRR = TwoMA(val_data , periods , small_MA , long_MA , init_money , invest_percent , print_graph = True)
    print("IRR : " , IRR)

    return IRR


from math import floor

def buy_stock(money, stock_price):
  stock= money/1.001425/stock_price
  return stock

def sell_stock(stock, stock_price):
  money = stock*stock_price - stock*stock_price*0.004425
  return money