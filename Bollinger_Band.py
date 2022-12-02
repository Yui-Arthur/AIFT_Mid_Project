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
import math
from AIFT_plotly_finance import *


def BollingerBand(data , period , MA_period , up_K , down_K , init_money , invest_percent , print_graph = False) :

    money = init_money
    stock = 0
    assets = init_money
    

    MA_index = 0
    MA_sum = 0
    MA_pow_sum = 1
    MA_days = 0
    last_MA = 0

    if print_graph:
        # history = pd.DataFrame(columns = ["Date" , "Money" , "Stock"])
        history = pd.DataFrame(columns = [ "Money" , "Stock"])
        history =  pd.concat([history , pd.Series([init_money , 0] , index =  ["Money" , "Stock"]).to_frame().T])
        # Boolinger_history = pd.DataFrame(columns = ["Date" , "up_line" , "mid_line" , "down_line"])
        Boolinger_history = pd.DataFrame(columns = ["up_line" , "mid_line" , "down_line"])
        Boolinger_history =  pd.concat([Boolinger_history , pd.Series([0 , 0 , 0] , index =  ["up_line" , "mid_line" , "down_line"]).to_frame().T])
        


        
    

    for index , row in data.iterrows():
        
        
        # 加上昨天的收盤價
        # print(index)
        if index == 0:
            continue

        MA_sum += data.loc[index - 1 , "Close"]
        MA_pow_sum += data.loc[index - 1 , "Close"]**2


        # 如果未滿MA天數就不推動index
        if MA_days == MA_period:
            MA_sum -= data.loc[MA_index , "Close"]
            MA_pow_sum -= data.loc[MA_index , "Close"]**2
            MA_index += 1
        else:
            MA_days += 1

        # MA_pow_sum = round(MA_pow_sum , 4)
        # MA_sum = math.floor(MA_sum , 5)
        # 標準差 = 平方的平均 - 平均的平方 開根號
        SD = ( (MA_pow_sum / MA_days) - (MA_sum / MA_days)**2 ) ** 0.5
        MA = (MA_sum / MA_days)
        # print("MA POW "  , MA_pow_sum , "MA Days " , MA_days , "MA Sum " , MA_sum , "SD ",SD)

        # 上軌 = 中軌 + X倍標準差
        up_line = MA + up_K * SD
        mid_line = MA
        down_line = MA - down_K * SD

        # print(f"{up_line} , {mid_line} , {down_line}")
        # 價格超過上軌做空
        if row["Close"] > up_line:
            money += stock * invest_percent * row["Close"]
            stock *= (1.0 - invest_percent)
        # 價格小於下軌做多
        elif row["Close"] < down_line:
            stock += money * invest_percent / row["Close"] 
            money *= (1.0 - invest_percent)


        assets = money + stock * row["Close"]

        

        if print_graph:
            history =  pd.concat([history , pd.Series([ money + stock * row["Close"], stock * row["Close"]] , index =  [ "Money" , "Stock" ]).to_frame().T])
            # history =  pd.concat([history , pd.Series([row["Date"] , money + stock * row["Close"], stock * row["Close"]] , index =  ["Date" , "Money" , "Stock" ]).to_frame().T])
            # Boolinger_history = pd.concat([Boolinger_history , pd.Series([row["Date"] , up_line , mid_line , down_line] , index =  ["Date" , "up_line" , "mid_line" , "down_line"]).to_frame().T])
            Boolinger_history = pd.concat([Boolinger_history , pd.Series([ up_line , mid_line , down_line] , index =  [ "up_line" , "mid_line" , "down_line"]).to_frame().T])
           
            # print(history)

    IRR = (((assets - init_money) / init_money + 1 ) ** (1 / period) - 1 ) * 100
    if print_graph:


        # fig.update_layout(
        #     title='損益表', title_x=0.5, #標題致中
        #     # yaxis=dict(tickformat="4f") #輸出型式
        # )
        # fig.show()
        Boolinger_history =  Boolinger_history.reset_index(drop = True)
        history =  history.reset_index(drop = True)
        # print (Boolinger_history)
        # print (history)

        all_data = pd.concat([data , Boolinger_history  , history] , axis = 1)
        # all_data = pd.concat([all_data , history] , axis = 1)
        # print(all_data)
        draw_Candlestick(all_data , draw_BollingerBands = True , save_path = f"BollingerBand_Candlestick_{10-period}-{period}")
        draw_accumulated_capital(all_data , save_path = f"BollingerBand_Money_{10-period}-{period}_{round(IRR,2)}")
        draw_combin_fig(all_data , draw_BollingerBands = True , save_path = f"BollingerBand_combin_{10-period}-{period}_{round(IRR,3)}")


    # print(time.perf_counter() - t )
    return IRR
    # return (assets - init_money) / init_money * 100
    
#解碼
def BollingerBand_decode(chromosome):
    # 29bit

    # MA 8 bit 1~256
    MA_period = int(chromosome[0:8], 2) + 2
    # up_K 7 bit 0 ~ 128
    up_K = 1 / 32 * int(chromosome[8:15], 2)
    # down_K 7 bit 0 ~ 128
    down_K = 1 / 32 * int(chromosome[15:23], 2)

    # 投資比例 7 bit (0~127)
    invest_percent = 100 / 127 * int(chromosome[23:], 2) / 100

    # number = [int(chromosome[0:8], 2) + 1 , int(chromosome[8:], 2) + 1]

    return MA_period , up_K , down_K , invest_percent

def BollingerBand_Fitness_Process(chromosome , training_data , period , init_money):


    MA_period , up_K , down_K , invest_percent = BollingerBand_decode(chromosome)
    IRR = BollingerBand(training_data , period , MA_period , up_K , down_K ,init_money , invest_percent)
    return IRR


def BollingerBand_validate ( best_chromosome , val_data , periods , init_money):
    MA_period , up_K , down_K , invest_percent = BollingerBand_decode(best_chromosome)
    print("MA_period : ", MA_period , "\nup_K: ", up_K , "\ndown_K" , down_K ,"\ninvest_percent : ", invest_percent)
    IRR = BollingerBand(val_data , periods , MA_period , up_K , down_K ,init_money , invest_percent , print_graph = True)
    print("IRR : " , IRR)
    
    return IRR



