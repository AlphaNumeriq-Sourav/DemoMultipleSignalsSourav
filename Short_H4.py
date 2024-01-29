import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
import MetaTrader5 as mt5
import time
from multiprocessing import pool , Process
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import schedule
import pandas_ta as ta
import warnings
import logging
warnings.filterwarnings("ignore")
import importlib
import sig_lib as sig
importlib.reload(sig)
from ba_signals import entry_signal1



# function to send a market order
def market_order(symbol, volume, order_type,comment,magic, **kwargs):
    tick = mt5.symbol_info_tick(symbol)
    order_dict = {'buy': 0, 'sell': 1}
    price_dict = {'buy': tick.ask, 'sell': tick.bid}

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": 2,
        "magic": magic,
        "comment":comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(request)

    return order_result





# function to close an order base don ticket id
def close_order(ticket):
    positions = mt5.positions_get()

    for pos in positions:
        tick = mt5.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 represents buy, 1 represents sell - inverting order_type to close the position
        price_dict = {0: tick.bid, 1: tick.ask}

        if pos.ticket == ticket:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": pos.ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": type_dict[pos.type],
                "price": price_dict[pos.type],
                "deviation": 2,
                
                
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            order_result = mt5.order_send(request)

            return order_result

    return 'Ticket does not exist'






# -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
# Function to Execute the Trades of EURUSD when a New signal comes from signal 1 and also to Exit the Trades Also
# -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------


def Execution(script_name,symbol , PerCentageRisk , SL_TpRatio ,TP,SL,pipval,logger ,Choices , ChoicesExitModels,  login , password , server):
    NoOfSignals = 1
    NoOfSignals +=1
    time_hr = (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time)- timedelta(hours=3))

    df = pd.DataFrame(mt5.copy_rates_from_pos(symbol ,mt5.TIMEFRAME_H4 , 0 , 2700))

    logger.debug(f'Running Event Loop of Instrument:{symbol} at ServerTime : {datetime.now()}  BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3)}  for the New Short Signal Modified by Sourav')

    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
    # Logic to Get the H4 DataFrame for the Instrument
    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------

    for i in range(2):
        try: 
            df = pd.DataFrame(mt5.copy_rates_from_pos(symbol ,mt5.TIMEFRAME_H4 , 0 , 2700))
            df['time']= df['time'].map(lambda Date : datetime.fromtimestamp(Date) -  timedelta(hours= 3))

            time_hr = (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time)- timedelta(hours=3))
            logger.debug(f"Checking DataFrameLastIndex and BrokerTime of Instrument : {symbol} BrokerTime: {time_hr} H4DfLastIndex : {df.iloc[-1]['time']}")

            for i in range(5):
                if  (df.iloc[-1]['time'].hour == time_hr.hour) or (df.iloc[-1]['time'].hour > time_hr.hour) or ((df.iloc[-1]['time'].hour == 0) and (time_hr.hour >=23)):
                     index = -2
                     break
                else:
                    df = pd.DataFrame(mt5.copy_rates_from_pos(symbol ,mt5.TIMEFRAME_H4, 0 , 2700))
                    index = -1
                    df['time']= df['time'].map(lambda Date : datetime.fromtimestamp(Date) -  timedelta(hours= 3))
                    time_false = (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time)- timedelta(hours=3))
                    logger.debug(f"Retrying getting Latest candle for H4data of Instrument : {symbol} FalseBrokerTime: {time_hr} H4DfLastIndex : {df.iloc[-1]['time']} NowBrokerTime : {time_false}")
                    if  (df.iloc[-1]['time'].hour == time_hr.hour) or (df.iloc[-1]['time'].hour > time_hr.hour) or ((df.iloc[-1]['time'].hour == 0) and (time_hr.hour >=23)):
                        index = -2
                

            
            
            df['ValueOpen'], df['ValueLow'], df['ValueHigh'], df['ValueClose'], df['WinsLast'] = \
            sig.ValueCharts(df,5,(1/SL_TpRatio),'open'), sig.ValueCharts(df,5,(1/SL_TpRatio),'low'), sig.ValueCharts(df,5,(1/SL_TpRatio),'high'), \
            sig.ValueCharts(df,5,(1/SL_TpRatio),'close'), sig.WinsLast(df, 5 , column='close')
            
            
            # ATR
            df['atr_7'] = sig.AvgTrueRange(df,7)
            df['CompositeATR'] = sig.CompositeATR(df , 2 , 24)
            
            
            # RSI
            df['rsi_14'] = sig.rsi(df,14)
            
            
            
            
            # OHLC
            df['OHLC'] = sig.OHLC(df)
            
            
            
            
            
            # SMA
            df['sma_5'], df['sma_20'] =\
            sig.SMA(df,5), sig.SMA(df,20)
            
            
            
            
            # EMA
            df['ema_2'] = sig.EMA(df , 2)
            
            
            # ADX
            df['adx_1'],  df['adx_2'], df['adx_3'],  df['adx_5'], df['adx_7'], df['adx_9'], df['adx_10'], df['adx_13'], df['adx_14'], df['adx_15'], df['adx_17'], df['adx_18'], df['adx_19'], df['adx_20']  = \
            sig.ADX(df, 1), sig.ADX(df, 2), sig.ADX(df, 3), sig.ADX(df, 5), sig.ADX(df, 7), sig.ADX(df, 9), sig.ADX(df, 10), sig.ADX(df, 13), sig.ADX(df, 14), sig.ADX(df, 15), sig.ADX(df, 17), sig.ADX(df, 18), sig.ADX(df, 19), sig.ADX(df, 20)
            
            
            
            
            
           

        except AttributeError:
            if mt5.initialize():
                logger.info(f'MT5 Connect Reestablished at BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3)}')
            else:
                logger.error(f'MT5 Connection Not able to connect at BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3)}  Again Trying......')

                mt5.initialize(login = login , password = password, server = server)
                #time.sleep(20)
                logger.debug(f'MT5 Connect Reestablished after Retry Status : {mt5.initialize()}  at BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3)}')
            continue
        break
    
    
    
    
    
    
    
    
    df.to_csv(f'{script_name}_dataframe')         
    df_entry = pd.DataFrame(columns =  ['signals','orderid','volume','price_open','TP','SL','TP1' , 'flag'])
    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
    # Logic to Push the Market Order to the Broker One we got any signals if we don't have active trade from the signals
    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
    
        
    for i in range(len(Choices)):
        df_open_signals = pd.read_csv(f'{symbol}_{script_name}_open_signals.csv' )
        signal = f'signal{Choices[i]}'
        
        if df_open_signals['ActiveChoice'].eq(Choices[i]).any():
            logger.debug(f'Signal{Choices[i]} Already have an active Trade of Instrument : {symbol} BrokerTime : {(datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time)- timedelta(hours=3))}')
            continue
        
        condition = entry_signal1(df,Choices[i],index)

        if condition:
            variable = ChoicesExitModels[i]
            # Got a Short Entry 
            if variable == 'Trail':
                flag = 0
                time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time)- timedelta(hours=3))
                logger.debug(f'Got Short Indication Candle for {signal} {symbol} at BrokerTime : {time1}')
                data = df.copy()
                logger.debug(f"{data.iloc[index]['close']} atr: {data.iloc[index]['atr_7']} ")


                SL_dis = SL
                LotSize = round((PerCentageRisk * mt5.account_info().equity)/(pipval*50),2)
                
                order= market_order(symbol , LotSize,'sell',signal,3001+Choices[i] )
                tick = mt5.symbol_info_tick(symbol)
                Price = tick.ask
                
                ATR = df.iloc[index]['atr_7']
                StopLoss = Price + (SL_dis * SL_TpRatio)
                TP_val = Price - (TP * SL_TpRatio)
                order_id = order.order
                order_price = order.price
                logger.info(f'Entry at {time1} for {symbol}  , SL : {StopLoss} , TP : {TP_val} ,Lotsize : {LotSize} , OrderPrice : {Price}, comment : {order.comment} Flag : {flag} OrderID : {order_id}')
                
                '''Updating the Entry DF'''
                df_entry.loc[len(df_entry)] = [Choices[i],order_id,order.volume,Price,TP_val,StopLoss,0,flag]
                
                '''Updating and Saving the ActiveSignals DF'''
                df_open_signals.loc[len(df_open_signals)] = [Choices[i]]
                df_open_signals.to_csv(f'{symbol}_{script_name}_open_signals.csv' , index=False)
            
            
        else:
            
            logger.debug(f"No entry for {signal} of Instrument : {symbol}  close : {df.iloc[index]['close']} at BrokerTime : {(datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3))}")  
        
            
            
                    
                    
                    
                    
    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
    # Logic to Exit the Short Trades if hits SL and also the trailing Part
    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
    if not df_entry.empty:
        logger.debug(f'Entry happened for {symbol} , Checking for Exit.....')
                        
        while True:
            if (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3)).weekday() == 5 or (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3)).weekday() ==6:
                continue
            
            if not  mt5.initialize():
                logger.debug("Mt5 Terminal Got Disconnected...")
                    
                time1 = (datetime.now())
                with open(f'NotInitial.txt' , 'a') as file:
                            file.write(f'\n symbol = {symbol},')
                            
                            file.write(f'Time = {time1}')
                file.close()
                time.sleep(10)
                cd = mt5.initialize(login = login , password = password, server = server)
                logger.debug(f'Is Connected : {cd}')
                continue
            
            
            Price = mt5.symbol_info_tick(symbol).ask
                
            for index, row in df_entry.iterrows(): 
                try:
                    
                    # If the Price hit SL
                    if Price >= row['SL']:
                            time_s = (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3))
                            #print(f'SL Hit at{time_s} ')
                            close = close_order(row['orderid'])
                            logger.info(f"SL hit Short BrokerTime : {time_s} SL : {row['SL']} TP : {row['TP']} ,{row['signals']},{close.comment}  ")
                            if close.comment == 'Request executed':
                                
                                '''Delete the Signals Trade from df_entry when we exit our Order'''
                                df_entry = df_entry.drop(index)
                                
                                
                                '''Update the OpenSignals Df to take the New trade from now on'''
                                df_open_signals = pd.read_csv(f'{symbol}_{script_name}_open_signals.csv' )
                                df_entry.reset_index(inplace= True)
                                df_entry.drop('index', axis=1, inplace=True)
                                df_open_signals = df_open_signals[df_open_signals.ActiveChoice!= row['signals']].reset_index(drop=True)
                                df_open_signals.to_csv(f'{symbol}_{script_name}_open_signals.csv' , index=False)
                                
                            elif close.comment == 'Ticket does not exist':
                                '''Delete the Signals Trade from df_entry when we exit our Order'''
                                df_entry = df_entry.drop(index)
                                logger.info(f'Manually Closed the order for {symbol} of OrderID : {row["orderid"]}')
                                
                                '''Update the OpenSignals Df to take the New trade from now on'''
                                df_open_signals = pd.read_csv(f'{symbol}_{script_name}_open_signals.csv' )
                                df_entry.reset_index(inplace= True)
                                df_entry.drop('index', axis=1, inplace=True)
                                df_open_signals = df_open_signals[df_open_signals.ActiveChoice!= row['signals']].reset_index(drop=True)
                                df_open_signals.to_csv(f'{symbol}_{script_name}_open_signals.csv' , index=False)
                                
                    
                    # First Trailing Step            
                    elif (Price <= row['TP']) and (row['flag'] == 0):
                        time_s = (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3))
                        row['SL'] = row['price_open'] - 1*(SL_TpRatio)
                        row['TP'] = row['TP'] - 1*(SL_TpRatio)
                        row['flag'] = 1
                        logger.info(f"First Trailing Step Hit at BrokerTime : {time_s} at CMP : {Price} , NewSL : {row['SL']} NewTP : {row['TP']} Flag : {row['flag']} of OrderID : {row['orderid']}")
                        
                    # Trailing SL and TP when we reaches new TP (note - this line of code will work only when First Trailing Step happened )
                    elif (Price <= row['TP']) and (row['flag'] == 1):
                        time_s = (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3))
                        row['SL'] = row['SL'] - 1*(SL_TpRatio)
                        row['TP'] = row['TP'] - 1*(SL_TpRatio)
                        logger.info(f"Trailing at BrokerTime : {time_s} at CMP : {Price} , NewSL : {row['SL']} NewTP : {row['TP']} Flag : {row['flag']} of OrderID : {row['orderid']}")
                        
                        
                except Exception as e:
                    logger.error(f'Error : {e}  When We are Exiting a Trade for {symbol}')
                    continue
                
                
                
            if len(df_entry) == 0:
                logger.debug(f'Function Out after the Exit trade of {symbol} at BrokerTime : {(datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3))}')
                break
                
    else:
        time.sleep(10)
        logger.debug(f'Function Out of {symbol} at BrokerTime : {(datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3))}') 
        
                    
        
                                        
                                        












