from skpy import Skype
from ba_signals import entry_signal1
import sig_lib as sig
import importlib
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta
import MetaTrader5 as mt5
import time
from multiprocessing import pool, Process
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import schedule
import pandas_ta as ta
import warnings
import logging
warnings.filterwarnings("ignore")
importlib.reload(sig)


user = 'sourav@purealphaventures.com'
pwd = 'Inno1691@1'
skype_connect = Skype(user, pwd)


# Function to send Skype Notification
def SendSkypeNotification(message, skype_connect):
    try:
        algo_trading_group = skype_connect.chats["19:10ccdc3f3fe74107b0bab4c9994f892a@thread.skype"]
        algo_trading_group.sendMsg(message)

    except Exception as e:
        user = 'sourav@purealphaventures.com'
        pwd = 'Inno1691@1'
        skype_connect = Skype(user, pwd)
        algo_trading_group = skype_connect.chats["19:10ccdc3f3fe74107b0bab4c9994f892a@thread.skype"]
        algo_trading_group.sendMsg(message)


# function to send a market order
def market_order(symbol, volume, order_type, comment, magic, **kwargs):
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
        "comment": comment,
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
        # 0 represents buy, 1 represents sell - inverting order_type to close the position
        type_dict = {0: 1, 1: 0}
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


def Execution_Short(script_name, symbol, PerCentageRisk, TP, SL, TrailTPPoints,SLTrailFirstSLPoint, logger, Choices, ChoicesExitModels,  login, password, server):
    HoursDelay = 3
    try:
        SL_TpRatio = mt5.symbol_info(symbol).point
        pipval = mt5.symbol_info(symbol).trade_tick_value_profit
        
        time_hr = (datetime.fromtimestamp(mt5.symbol_info_tick(
            symbol).time) - timedelta(hours=HoursDelay))
        df = pd.DataFrame(mt5.copy_rates_from_pos(
            symbol, mt5.TIMEFRAME_H4, 0, 2700))
        BrokerTime = datetime.fromtimestamp(mt5.symbol_info_tick(
            symbol).time) - timedelta(hours=HoursDelay)
    except AttributeError:
        if mt5.initialize():
            logger.info(
                f'MT5 Connect Reestablished at BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay)}')
            Execution_Short(script_name, symbol, PerCentageRisk, TP, SL, TrailTPPoints,
                      logger, Choices, ChoicesExitModels,  login, password, server)
        else:
            time.sleep(5)
            logger.error(
                f'MT5 Connection Not able to connect at ServerTime : {datetime.now()}  Again Trying......')
            SendSkypeNotification(
                f'MT5 Connection Not able to connect at ServerTime : {datetime.now()}  Again Trying......', skype_connect)
            mt5.initialize(login=login, password=password, server=server)
            logger.debug(
                f'MT5 Connect Reestablished after Retry Status : {mt5.initialize()}  at BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay)}')
            SendSkypeNotification(
                f'MT5 Connect Reestablished after Retry Status : {mt5.initialize()}  at BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay)}', skype_connect)
            Execution_Short(script_name, symbol, PerCentageRisk, TP, SL, TrailTPPoints,
                      logger, Choices, ChoicesExitModels,  login, password, server)

    # logger.debug(
    #     f'Running Event Loop of Instrument:{symbol} at ServerTime : {datetime.now()}  BrokerTime : {BrokerTime}  for the New Short Signal Modified by Sourav')

    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
    # Logic to Get the H4 DataFrame for the Instrument
    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------

    for i in range(2):
        try:
            df = pd.DataFrame(mt5.copy_rates_from_pos(
                symbol, mt5.TIMEFRAME_H4, 0, 2700))
            df['time'] = df['time'].map(lambda Date: datetime.fromtimestamp(
                Date) - timedelta(hours=HoursDelay))

            time_hr = (datetime.fromtimestamp(mt5.symbol_info_tick(
                symbol).time) - timedelta(hours=HoursDelay))
            # logger.debug(
            #     f"Checking DataFrameLastIndex and BrokerTime of Instrument : {symbol} BrokerTime: {time_hr} H4DfLastIndex : {df.iloc[-1]['time']}")

            for i in range(5):
                if (df.iloc[-1]['time'].hour == time_hr.hour) or (df.iloc[-1]['time'].hour > time_hr.hour) or ((df.iloc[-1]['time'].hour == 0) and (time_hr.hour >= 23)):
                    index = -2
                    break
                else:
                    df = pd.DataFrame(mt5.copy_rates_from_pos(
                        symbol, mt5.TIMEFRAME_H4, 0, 2700))
                    index = -1
                    df['time'] = df['time'].map(lambda Date: datetime.fromtimestamp(
                        Date) - timedelta(hours=HoursDelay))
                    time_false = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                    # logger.debug(
                    #     f"Retrying getting Latest candle for H4data of Instrument : {symbol} FalseBrokerTime: {time_hr} H4DfLastIndex : {df.iloc[-1]['time']} NowBrokerTime : {time_false}")
                    if (df.iloc[-1]['time'].hour == time_hr.hour) or (df.iloc[-1]['time'].hour > time_hr.hour) or ((df.iloc[-1]['time'].hour == 0) and (time_hr.hour >= 23)):
                        index = -2

            

            df['ValueOpen'], df['ValueLow'], df['ValueHigh'], df['ValueClose'], df['WinsLast'] = \
                sig.ValueCharts(df, 5, 'open'), sig.ValueCharts(df, 5, 'low'), sig.ValueCharts(df, 5, 'high'), \
                sig.ValueCharts(df, 5, 'close'), sig.WinsLast(
                    df, 5, column='close')

            # ATR
            df['atr_7'] = sig.AvgTrueRange(df, 7)
            df['CompositeATR_2_24'] = sig.CompositeATR(df, 2, 24)
            df['CompositeRSI_2_24'] = sig.CompositeRSI(df,2,24)
            df['AvgTrueRange_10'] = sig.AvgTrueRange(df,10,"high","low","close")
            df['CompositeSMA'] = sig.CompositeSMA(df,8,20,50,200)
            df['CompositeEMA'] = sig.CompositeEMA(df,8,20,50,200)
            
            df['rateOfChange_close_10'] = sig.rateOfChange(df , 10  , SL_TpRatio,'close')
            df['CubeHLC'] = sig.CubeHLC(df,'high','low','close')
            df['PivotPoint'] = sig.pivotpoint(df,'high','low', 'close')
            df['momentum_close_5'] = sig.momentum(df,5,'close')

            # RSI
            df['rsi_14'] = sig.rsi(df, 14)
            df['rsi_2'] = sig.rsi(df, 2)

            # OHLC
            df['OHLC'] = sig.OHLC(df)

            # SMA
            df['sma_5'], df['sma_10'] , df['sma_20'] =\
                sig.SMA(df, 5), sig.SMA(df, 10) , sig.SMA(df, 20)

            # EMA
            df['ema_2'] = sig.EMA(df, 2)
            df['ema_3'] = sig.EMA(df, 3)
            df['ema_1'] = sig.EMA(df, 1)

            # ADX
            df['adx_1'],  df['adx_2'], df['adx_3'] , df['adx_4'],  df['adx_5'], df['adx_7'], df['adx_9'], df['adx_10'], df['adx_13'], df['adx_14'], df['adx_15'], df['adx_17'], df['adx_18'], df['adx_19'], df['adx_20'] = \
                sig.ADX(df, 1), sig.ADX(df, 2), sig.ADX(df, 3) , sig.ADX(df, 4), sig.ADX(df, 5), sig.ADX(df, 7), sig.ADX(df, 9), sig.ADX(df, 10), sig.ADX(
                    df, 13), sig.ADX(df, 14), sig.ADX(df, 15), sig.ADX(df, 17), sig.ADX(df, 18), sig.ADX(df, 19), sig.ADX(df, 20)

        except AttributeError:
            time.sleep(5)
            if mt5.initialize():
                logger.info(
                    f'MT5 Connect Reestablished at BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay)}')
            else:
                logger.error(
                    f'MT5 Connection Not able to connect at ServerTime : {datetime.now()}  Again Trying......')
                SendSkypeNotification(
                    f'MT5 Connection Not able to connect at ServerTime : {datetime.now()}  Again Trying......', skype_connect)
                mt5.initialize(login=login, password=password, server=server)
                # time.sleep(20)
                logger.debug(
                    f'MT5 Connect Reestablished after Retry Status : {mt5.initialize()}  at BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay)}')
                SendSkypeNotification(
                    f'MT5 Connect Reestablished after Retry Status : {mt5.initialize()}  at BrokerTime : {datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay)}', skype_connect)
            continue
        break

    df.to_csv(f'{script_name}_dataframe')
    df_entry = pd.DataFrame(
        columns=['signals', 'orderid', 'volume', 'price_open', 'TP', 'SL', 'TP1', 'flag'])
    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
    # Logic to Push the Market Order to the Broker One we got any signals if we don't have active trade from the signals
    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------

    for i in range(len(Choices)):
        df_open_signals = pd.read_csv(
            f'{symbol}_{script_name}_open_signals.csv')
        signal = f'signal{Choices[i]}'
        Signal_uni_name = f"{symbol}_{Choices[i]}_Short_{ChoicesExitModels[i]}"

        if df_open_signals['ActiveChoice'].eq(Choices[i]).any():
            logger.debug(
                f'Signal{Choices[i]} Already have an active Trade of Instrument : {symbol} ServerTime : {datetime.now()}')
            continue

        condition = entry_signal1(df, Choices[i], index)

        if condition:
            variable = ChoicesExitModels[i]
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
            # Trail
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------

            if variable == 'Trail':
                flag = 0
                try:
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                except AttributeError:
                    time.sleep(2)
                    mt5.initialize(
                        login=login, password=password, server=server)
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                data = df.copy()
                logger.debug(
                    f'Got Short Indication Candle for {signal} {symbol} at BrokerTime : {time1} ClosePrice : {data.iloc[index]["close"]} atr: {data.iloc[index]["atr_7"]}')
                
                
                LotSize = round(
                    (PerCentageRisk * mt5.account_info().equity)/(pipval*SL), 2)
                
                if symbol == "XTIUSD":
                        LotSize = float(round(
                        (PerCentageRisk * mt5.account_info().equity)/(pipval*SL)))

                while True:
                    if not mt5.initialize():
                        logger.debug(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}")
                        SendSkypeNotification(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}", skype_connect)

                        time1 = (datetime.now())
                        with open(f'NotInitial.txt', 'a') as file:
                            file.write(f'\n symbol = {symbol},')

                            file.write(f'Time = {time1}')
                        file.close()
                        time.sleep(10)
                        cd = mt5.initialize(
                            login=login, password=password, server=server)
                        logger.debug(f'Is Connected : {cd}')
                        SendSkypeNotification(
                            f"Is Connection Reestablished : {cd} ", skype_connect)
                        continue

                    order = market_order(
                        symbol, LotSize, 'sell', Signal_uni_name, 3001+Choices[i])
                    time.sleep(1)
                    if order.comment == 'Market closed':
                        time.sleep(1)
                        continue
                    break

                
                

                ATR = df.iloc[index]['atr_7']
                Price  = order.price
                StopLoss = Price + (SL * SL_TpRatio)
                TP_val = Price - (TP * SL_TpRatio)
                order_id = order.order
                
                logger.info(
                        f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}')
                SendSkypeNotification(
                        f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}', skype_connect)
                '''Updating the Entry DF'''
                df_entry.loc[len(df_entry)] = [
                    Choices[i], order_id, order.volume, Price, TP_val, StopLoss, 0, flag]

                '''Updating and Saving the ActiveSignals DF'''
                df_open_signals.loc[len(df_open_signals)] = [Choices[i]]
                df_open_signals.to_csv(
                    f'{symbol}_{script_name}_open_signals.csv', index=False)
                
                
                
                
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
            # ATR
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
            elif variable == 'ATR':
                flag = 2
                try:
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                except AttributeError:
                    time.sleep(2)
                    mt5.initialize(
                        login=login, password=password, server=server)
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                data = df.copy()
                logger.debug(
                f'Got Short Indication Candle for {signal} {symbol} at BrokerTime : {time1} ClosePrice : {data.iloc[index]["close"]} atr: {data.iloc[index]["atr_7"]}')
                
                
                StopLossInPip = (data.iloc[index]['atr_7']/SL_TpRatio) * 3

                LotSize = round(
                    (PerCentageRisk * mt5.account_info().equity)/(pipval*StopLossInPip), 2)
                
                if symbol == "XTIUSD":
                    LotSize = float(round(
                    (PerCentageRisk * mt5.account_info().equity)/(pipval*SL)))

                while True:
                    if not mt5.initialize():
                        logger.debug(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}")
                        SendSkypeNotification(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}", skype_connect)

                        time1 = (datetime.now())
                        with open(f'NotInitial.txt', 'a') as file:
                            file.write(f'\n symbol = {symbol},')

                            file.write(f'Time = {time1}')
                        file.close()
                        time.sleep(10)
                        cd = mt5.initialize(
                            login=login, password=password, server=server)
                        logger.debug(f'Is Connected : {cd}')
                        SendSkypeNotification(
                            f"Is Connection Reestablished : {cd} ", skype_connect)
                        continue

                    order = market_order(
                        symbol, LotSize, 'sell', Signal_uni_name, 3001+Choices[i])
                    time.sleep(1)
                    if order.comment == 'Market closed':
                        time.sleep(1)
                        continue
                    break


                ATR = df.iloc[index]['atr_7']
                Price  = order.price
                StopLoss = Price + (2* ATR)
                TP_val = Price - (3 * ATR)
                order_id = order.order
                logger.info(
                    f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}')
                SendSkypeNotification(
                    f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}', skype_connect)
                '''Updating the Entry DF'''
                df_entry.loc[len(df_entry)] = [
                    Choices[i], order_id, order.volume, Price, TP_val, StopLoss, 0, flag]

                '''Updating and Saving the ActiveSignals DF'''
                df_open_signals.loc[len(df_open_signals)] = [Choices[i]]
                df_open_signals.to_csv(
                    f'{symbol}_{script_name}_open_signals.csv', index=False)
                
                
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
            # Fixed
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
                    
            elif variable == 'Fixed':
                flag = 2
                try:
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                except AttributeError:
                    time.sleep(2)
                    mt5.initialize(
                        login=login, password=password, server=server)
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                data = df.copy()
                logger.debug(
                f'Got Short Indication Candle for {signal} {symbol} at BrokerTime : {time1} ClosePrice : {data.iloc[index]["close"]} atr: {data.iloc[index]["atr_7"]}')
                
                
                

                LotSize = round(
                    (PerCentageRisk * mt5.account_info().equity)/(pipval*SL), 2)
                if symbol == "XTIUSD":
                    LotSize = float(round(
                    (PerCentageRisk * mt5.account_info().equity)/(pipval*SL)))

                while True:
                    if not mt5.initialize():
                        logger.debug(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}")
                        SendSkypeNotification(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}", skype_connect)

                        time1 = (datetime.now())
                        with open(f'NotInitial.txt', 'a') as file:
                            file.write(f'\n symbol = {symbol},')

                            file.write(f'Time = {time1}')
                        file.close()
                        time.sleep(10)
                        cd = mt5.initialize(
                            login=login, password=password, server=server)
                        logger.debug(f'Is Connected : {cd}')
                        SendSkypeNotification(
                            f"Is Connection Reestablished : {cd} ", skype_connect)
                        continue

                    order = market_order(
                        symbol, LotSize, 'sell', Signal_uni_name, 3001+Choices[i])
                    time.sleep(1)
                    if order.comment == 'Market closed':
                        time.sleep(1)
                        continue
                    break


                ATR = df.iloc[index]['atr_7']
                Price  = order.price
                StopLoss = Price + (SL * SL_TpRatio)
                TP_val = Price - (TP * SL_TpRatio)
                order_id = order.order
                logger.info(
                    f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}')
                SendSkypeNotification(
                    f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}', skype_connect)
                '''Updating the Entry DF'''
                df_entry.loc[len(df_entry)] = [
                    Choices[i], order_id, order.volume, Price, TP_val, StopLoss, 0, flag]

                '''Updating and Saving the ActiveSignals DF'''
                df_open_signals.loc[len(df_open_signals)] = [Choices[i]]
                df_open_signals.to_csv(
                    f'{symbol}_{script_name}_open_signals.csv', index=False)
                
                    
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
            # Trail_ATR
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------  
            elif variable == 'Trail_ATR':
                flag = 0
                try:
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                except AttributeError:
                    time.sleep(2)
                    mt5.initialize(
                        login=login, password=password, server=server)
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                data = df.copy()
                logger.debug(
                f'Got Short Indication Candle for {signal} {symbol} at BrokerTime : {time1} ClosePrice : {data.iloc[index]["close"]} atr: {data.iloc[index]["atr_7"]}')
                
                StopLossInPip = (data.iloc[index]['atr_7']/SL_TpRatio) * 3
                

                LotSize = round(
                    (PerCentageRisk * mt5.account_info().equity)/(pipval*StopLossInPip), 2)
                if symbol == "XTIUSD":
                    LotSize = float(round(
                    (PerCentageRisk * mt5.account_info().equity)/(pipval*StopLossInPip)))

                while True:
                    if not mt5.initialize():
                        logger.debug(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}")
                        SendSkypeNotification(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}", skype_connect)

                        time1 = (datetime.now())
                        with open(f'NotInitial.txt', 'a') as file:
                            file.write(f'\n symbol = {symbol},')

                            file.write(f'Time = {time1}')
                        file.close()
                        time.sleep(10)
                        cd = mt5.initialize(
                            login=login, password=password, server=server)
                        logger.debug(f'Is Connected : {cd}')
                        SendSkypeNotification(
                            f"Is Connection Reestablished : {cd} ", skype_connect)
                        continue

                    order = market_order(
                        symbol, LotSize, 'sell', Signal_uni_name, 3001+Choices[i])
                    time.sleep(1)
                    if order.comment == 'Market closed':
                        time.sleep(1)
                        continue
                    break


                
                ATR = df.iloc[index]['atr_7']
                Price  = order.price
                StopLoss = Price + (2* ATR)
                TP_val = Price - (3 * ATR)
                order_id = order.order
                
                
                logger.info(
                    f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}')
                SendSkypeNotification(
                    f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}', skype_connect)
                '''Updating the Entry DF'''
                df_entry.loc[len(df_entry)] = [
                    Choices[i], order_id, order.volume, Price, TP_val, StopLoss, 0, flag]

                '''Updating and Saving the ActiveSignals DF'''
                df_open_signals.loc[len(df_open_signals)] = [Choices[i]]
                df_open_signals.to_csv(
                    f'{symbol}_{script_name}_open_signals.csv', index=False)
                
        
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
            # SL_Trail
            # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
            elif variable == 'SL_Trail':
                flag = 3
                try:
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                    tick = mt5.symbol_info_tick(symbol)
                except AttributeError:
                    time.sleep(2)
                    mt5.initialize(
                        login=login, password=password, server=server)
                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(
                        symbol).time) - timedelta(hours=HoursDelay))
                    tick = mt5.symbol_info_tick(symbol)
                data = df.copy()
                logger.debug(
                f'Got Short Indication Candle for {signal} {symbol} at BrokerTime : {time1} ClosePrice : {data.iloc[index]["close"]} atr: {data.iloc[index]["atr_7"]}')
                
                
                Price = tick.bid
                StopLossInPip = ((0.5/100) * Price)/SL_TpRatio


                LotSize = round(
                    (PerCentageRisk * mt5.account_info().equity)/(pipval*StopLossInPip), 2)
                if symbol == "XTIUSD":
                    LotSize = float(round(
                    (PerCentageRisk * mt5.account_info().equity)/(pipval*StopLossInPip)))

                while True:
                    if not mt5.initialize():
                        logger.debug(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}")
                        SendSkypeNotification(
                            f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}", skype_connect)

                        time1 = (datetime.now())
                        with open(f'NotInitial.txt', 'a') as file:
                            file.write(f'\n symbol = {symbol},')

                            file.write(f'Time = {time1}')
                        file.close()
                        time.sleep(10)
                        cd = mt5.initialize(
                            login=login, password=password, server=server)
                        logger.debug(f'Is Connected : {cd}')
                        SendSkypeNotification(
                            f"Is Connection Reestablished : {cd} ", skype_connect)
                        continue

                    order = market_order(
                        symbol, LotSize, 'sell', Signal_uni_name, 3001+Choices[i])
                    time.sleep(1)
                    if order.comment == 'Market closed':
                        time.sleep(1)
                        continue
                    break


                
                ATR = df.iloc[index]['atr_7']
                Price  = order.price
                StopLoss = Price + ((0.5/100) * Price)
                TP_val = Price - ((0.5/100) * Price)
                TP1 = Price - ((0.25/100) * Price)
                order_id = order.order
                
                
                logger.info(
                    f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}')
                SendSkypeNotification(
                    f'Entry Short at {time1} for SignalID : {Signal_uni_name}  at EntryPrice : {Price}  StopLoss : {StopLoss} Target : {TP_val} Lotsize : {LotSize} ATR Value : {ATR} OrderComment : {order.comment} Flag : {flag} OrderID : {order_id}', skype_connect)
                '''Updating the Entry DF'''
                df_entry.loc[len(df_entry)] = [
                    Choices[i], order_id, order.volume, Price, TP_val, StopLoss, TP1, flag]

                '''Updating and Saving the ActiveSignals DF'''
                df_open_signals.loc[len(df_open_signals)] = [Choices[i]]
                df_open_signals.to_csv(
                    f'{symbol}_{script_name}_open_signals.csv', index=False)
        else:

            logger.debug(
                f"No entry for {signal} of Instrument : {symbol}  close : {df.iloc[index]['close']} at BrokerTime : {(datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay))}")

    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
    # Logic to Exit the Short Trades if hits SL and also the trailing Part
    # -------------------------x-----------------------x---------------------------x---------------------------x---------------------------x---------------------------
    if not df_entry.empty:
        # logger.debug(f'Entry happened for {symbol} , Checking for Exit.....')

        while True:
            if not mt5.initialize():
                logger.debug(
                    f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}")
                SendSkypeNotification(
                    f"Mt5 Terminal Got Disconnected... at {datetime.now()} for Symbol : {symbol}", skype_connect)

                time1 = (datetime.now())
                with open(f'NotInitial.txt', 'a') as file:
                    file.write(f'\n symbol = {symbol},')

                    file.write(f'Time = {time1}')
                file.close()
                time.sleep(10)
                cd = mt5.initialize(
                    login=login, password=password, server=server)
                logger.debug(f'Is Connected : {cd}')
                SendSkypeNotification(
                    f"Is Connection Reestablished : {cd} ", skype_connect)
                continue

            # Error here
            if (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay)).weekday() == 5 or (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay)).weekday() == 6:
                continue

            # Error Here
            Price = mt5.symbol_info_tick(symbol).ask

            for index, row in df_entry.iterrows():
                try:
                    ## For Manual Close Order Prevention
                    ActivePos = [pos.ticket for pos in mt5.positions_get()]
                    
                    if row['orderid'] not in ActivePos:
                        '''Delete the Signals Trade from df_entry when we exit our Order'''
                        df_entry = df_entry.drop(index)
                        logger.info(
                            f'Manually Closed the order for {symbol} of OrderID : {row["orderid"]}')
                        SendSkypeNotification(
                            f'Manually Closed the order for {symbol} of OrderID : {row["orderid"]}', skype_connect)

                        '''Update the OpenSignals Df to take the New trade from now on'''
                        df_open_signals = pd.read_csv(
                            f'{symbol}_{script_name}_open_signals.csv')
                        df_entry.reset_index(inplace=True)
                        df_entry.drop('index', axis=1, inplace=True)
                        df_open_signals = df_open_signals[df_open_signals.ActiveChoice != row['signals']].reset_index(
                            drop=True)
                        df_open_signals.to_csv(
                            f'{symbol}_{script_name}_open_signals.csv', index=False)

                    # If the Price hit SL
                    if Price >= row['SL']:
                        time_s = (datetime.fromtimestamp(mt5.symbol_info_tick(
                            symbol).time) - timedelta(hours=HoursDelay))
                        # print(f'SL Hit at{time_s} ')
                        close = close_order(row['orderid'])
                        logger.info(
                            f"SL hit for {symbol} Short BrokerTime : {time_s} SL : {row['SL']} TP : {row['TP']} ,Signal : {row['signals']} CloseOrderComment : {close.comment}")
                        SendSkypeNotification(
                            f"SL hit for {symbol} Short BrokerTime : {time_s} SL : {row['SL']} TP : {row['TP']} ,Signal : {row['signals']} CloseOrderComment : {close.comment}", skype_connect)
                        if close.comment == 'Request executed':

                            '''Delete the Signals Trade from df_entry when we exit our Order'''
                            df_entry = df_entry.drop(index)

                            '''Update the OpenSignals Df to take the New trade from now on'''
                            df_open_signals = pd.read_csv(
                                f'{symbol}_{script_name}_open_signals.csv')
                            df_entry.reset_index(inplace=True)
                            df_entry.drop('index', axis=1, inplace=True)
                            df_open_signals = df_open_signals[df_open_signals.ActiveChoice != row['signals']].reset_index(
                                drop=True)
                            df_open_signals.to_csv(
                                f'{symbol}_{script_name}_open_signals.csv', index=False)

                        elif close.comment == 'Ticket does not exist':
                            '''Delete the Signals Trade from df_entry when we exit our Order'''
                            df_entry = df_entry.drop(index)
                            logger.info(
                                f'Manually Closed the order for {symbol} of OrderID : {row["orderid"]}')
                            SendSkypeNotification(
                                f'Manually Closed the order for {symbol} of OrderID : {row["orderid"]}', skype_connect)

                            '''Update the OpenSignals Df to take the New trade from now on'''
                            df_open_signals = pd.read_csv(
                                f'{symbol}_{script_name}_open_signals.csv')
                            df_entry.reset_index(inplace=True)
                            df_entry.drop('index', axis=1, inplace=True)
                            df_open_signals = df_open_signals[df_open_signals.ActiveChoice != row['signals']].reset_index(
                                drop=True)
                            df_open_signals.to_csv(
                                f'{symbol}_{script_name}_open_signals.csv', index=False)

                    # First Trailing Step
                    elif (Price <= row['TP']) and (row['flag'] == 0):
                        time_s = (datetime.fromtimestamp(mt5.symbol_info_tick(
                            symbol).time) - timedelta(hours=HoursDelay))
                        row['SL'] = row['price_open'] - \
                            TrailTPPoints*(SL_TpRatio)
                        row['TP'] = row['TP'] - TrailTPPoints*(SL_TpRatio)
                        row['flag'] = 1
                        logger.info(
                            f"First Trailing Step Hit at BrokerTime : {time_s} at CMP : {Price} , NewSL : {row['SL']} NewTP : {row['TP']} Flag : {row['flag']} of OrderID : {row['orderid']}")
                        SendSkypeNotification(
                            f"First Trailing Step Hit for {symbol} of Signal : {row['signals']} at BrokerTime : {time_s} at CMP : {Price} , NewSL : {row['SL']} NewTP : {row['TP']} Flag : {row['flag']} of OrderID : {row['orderid']}", skype_connect)
                        
                    # For SL Trail Model
                    elif (Price <= row['TP1']) and (row['flag'] == 3):
                        time_s = (datetime.fromtimestamp(mt5.symbol_info_tick(
                            symbol).time) - timedelta(hours=HoursDelay))
                        row['SL'] = row['TP1'] + (SLTrailFirstSLPoint * SL_TpRatio)
                        row['TP'] = row['TP'] - ( TrailTPPoints*SL_TpRatio)
                        row['flag'] = 1
                        logger.info(
                            f"First Trailing Step Hit at BrokerTime : {time_s} at CMP : {Price} , NewSL : {row['SL']} NewTP : {row['TP']} Flag : {row['flag']} of OrderID : {row['orderid']}")
                        SendSkypeNotification(
                            f"First Trailing Step Hit for {symbol} of Signal : {row['signals']} at BrokerTime : {time_s} at CMP : {Price} , NewSL : {row['SL']} NewTP : {row['TP']} Flag : {row['flag']} of OrderID : {row['orderid']}", skype_connect)
                    
                    # For Fixed and ATR Model Tp Exit  
                    elif (Price <= row['TP']) and (row['flag'] == 2):
                        time_s = (datetime.fromtimestamp(mt5.symbol_info_tick(
                            symbol).time) - timedelta(hours=HoursDelay))
                        # print(f'SL Hit at{time_s} ')
                        close = close_order(row['orderid'])
                        logger.info(
                            f"Target hit for {symbol} Short BrokerTime : {time_s} SL : {row['SL']} TP : {row['TP']} ,Signal : {row['signals']} CloseOrderComment : {close.comment}")
                        SendSkypeNotification(
                            f"Target hit for {symbol} Short BrokerTime : {time_s} SL : {row['SL']} TP : {row['TP']} ,Signal : {row['signals']} CloseOrderComment : {close.comment}", skype_connect)
                        if close.comment == 'Request executed':

                            '''Delete the Signals Trade from df_entry when we exit our Order'''
                            df_entry = df_entry.drop(index)

                            '''Update the OpenSignals Df to take the New trade from now on'''
                            df_open_signals = pd.read_csv(
                                f'{symbol}_{script_name}_open_signals.csv')
                            df_entry.reset_index(inplace=True)
                            df_entry.drop('index', axis=1, inplace=True)
                            df_open_signals = df_open_signals[df_open_signals.ActiveChoice != row['signals']].reset_index(
                                drop=True)
                            df_open_signals.to_csv(
                                f'{symbol}_{script_name}_open_signals.csv', index=False)

                        elif close.comment == 'Ticket does not exist':
                            '''Delete the Signals Trade from df_entry when we exit our Order'''
                            df_entry = df_entry.drop(index)
                            logger.info(
                                f'Manually Closed the order for {symbol} of OrderID : {row["orderid"]}')
                            SendSkypeNotification(
                                f'Manually Closed the order for {symbol} of OrderID : {row["orderid"]}', skype_connect)

                            '''Update the OpenSignals Df to take the New trade from now on'''
                            df_open_signals = pd.read_csv(
                                f'{symbol}_{script_name}_open_signals.csv')
                            df_entry.reset_index(inplace=True)
                            df_entry.drop('index', axis=1, inplace=True)
                            df_open_signals = df_open_signals[df_open_signals.ActiveChoice != row['signals']].reset_index(
                                drop=True)
                            df_open_signals.to_csv(
                                f'{symbol}_{script_name}_open_signals.csv', index=False)


                    # Trailing SL and TP when we reaches new TP (note - this line of code will work only when First Trailing Step happened )
                    elif (Price <= row['TP']) and (row['flag'] == 1):
                        time_s = (datetime.fromtimestamp(mt5.symbol_info_tick(
                            symbol).time) - timedelta(hours=HoursDelay))
                        row['SL'] = row['SL'] - TrailTPPoints*(SL_TpRatio)
                        row['TP'] = row['TP'] - TrailTPPoints*(SL_TpRatio)
                        logger.info(
                            f"Trailing for {symbol} of Signal : {row['signals']} at BrokerTime : {time_s} at CMP : {Price} , NewSL : {row['SL']} NewTP : {row['TP']} Flag : {row['flag']} of OrderID : {row['orderid']}")
                        SendSkypeNotification(
                            f"Trailing for {symbol} of Signal : {row['signals']} at BrokerTime : {time_s} at CMP : {Price} , NewSL : {row['SL']} NewTP : {row['TP']} Flag : {row['flag']} of OrderID : {row['orderid']}", skype_connect)

                except Exception as e:
                    logger.error(
                        f'Error : {e}  When We are Exiting a Trade for {symbol}')
                    SendSkypeNotification(
                        f'Error : {e}  When We are Exiting a Trade for {symbol} at Time : {datetime.now()}', skype_connect)
                    continue

            if len(df_entry) == 0:
                logger.debug(
                    f'Function Out after the Exit trade of {symbol} at BrokerTime : {(datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay))}')
                break

    else:
        time.sleep(10)
        logger.debug(
            f'Function Out of {symbol} at BrokerTime : {(datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=HoursDelay))}')
