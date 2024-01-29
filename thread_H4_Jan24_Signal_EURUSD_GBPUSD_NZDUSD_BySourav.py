import threading
import importlib

import time


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
warnings.filterwarnings("ignore")
import importlib
import sig_lib as sig
importlib.reload(sig)
from Logging import setup_logger
import logging
import math
from config import thread_H4_Jan24_Signal_EURUSD_GBPUSD_NZDUSD_BySourav
from Short_H4 import Execution




'''Function to Run Instrument Signal file with a Independent Thread'''
def run_script(script_name,symbol , RISK , ds ,TP,SL,pip ,Choices , ChoicesExitModels, login , password , server ):
    logger = logging.getLogger(symbol)
    try:
        #script_module = importlib.import_module(script_name)
        Execution(script_name,symbol , RISK , ds ,TP,SL,pip,logger ,Choices , ChoicesExitModels,  login , password , server)
    except ImportError:
        logger.error(f"Failed to Import : {script_name}")




'''Function to create EntrySignalCsv Files and Logger File'''
def files(script_name,symbol , RISK , ds ,TP,SL,pip, Choices , ChoicesExitModels):
    # df_cols = ['signals','orderid','volume','price_open','TP','SL']
        
    # df_entry = pd.DataFrame(columns= df_cols) 
    # df_entry.to_csv(f'{script_name}_entry_signals.csv',index= False)
    
    df_open_signal = pd.DataFrame(columns = ['ActiveChoice'])
    df_open_signal.to_csv(f'{symbol}_{script_name}_open_signals.csv' , index=False)
    
    setup_logger(f'{symbol}_BA_H4_AddedBySourav.log' , symbol)


    
     
''''Main Function to run the Signal Script File Every 4 Hour from Monday to Friday'''
def PreMain():
    login = 25088141
    password = 'N3W*f%Ts??kF'
    server = 'Tickmill-Demo'
    path = r'C:\Program Files\MetaTrader 5\terminal64.exe'
    mt5.initialize( login = login , password = password, server = server)
    setup_logger('thread_H4_Jan24_Signal_EURUSD_GBPUSD_NZDUSD_BySourav.log' , 'MainLogfile')
    MainLogger = logging.getLogger('MainLogfile')
    #MainLogger.error('sss')
    
    
    script_args = thread_H4_Jan24_Signal_EURUSD_GBPUSD_NZDUSD_BySourav
    #print(script_args)
    for script_name, args in script_args.items():
        symbol = args[0]
        files(script_name,*args)
        # thread = threading.Thread(target=run_script, args=(script_name, *args , login , password , server))
        # thread.start()

        


        
    if mt5.initialize(login = login , password = password, server = server):
        MainLogger.debug(f'Script Started for thread_H4_Jan24_Signal_EURUSD_GBPUSD_NZDUSD_BySourav')
        while True:
            if (datetime.now().weekday()) != 5 and    \
                        (datetime.now().weekday()) != 6:
                if mt5.initialize():
                
                    if ((datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3)).weekday()) != 5 and ((datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3)).weekday()) != 6:
            
                        try:
                            time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=1))
                            time2 = mt5.symbol_info_tick(symbol).time
                            time3 = mt5.symbol_info_tick(symbol).time
                        except AttributeError:
                            time.sleep(20)
                            
                            
                        '''For all 4 Hour Timeframe apart from 0th Hour'''
                        if  (time2 % (3600 *24)  != 0) :  #not 00:00

                            if (time2 % (3600*4)  == 0) or (time2 % (3600*4)  < 30):
                                    for script_name, args in script_args.items():
                                        # create_file(script_name)  # Create a file for each script
                                        symbol = args[0]
                                        logger = logging.getLogger(symbol)
                                        #setup_logger(f'{symbol}_BA_H4_AddedBySourav.log')
                                        logger.debug(f'AT the next Hour InTime -- SymbolName : {symbol} BrokerTime : {time1}')
                                        thread = threading.Thread(target=run_script, args=(script_name, *args , login , password , server))
                                        thread.start()
                                    
                                    time.sleep(60)
                                    logger.debug(f'AT the next Hour OutTime -- SymbolName : {symbol} BrokerTime : {time1}')
                        
                        
                        '''For the Next Day 0th Hour candle Execution Code'''
                        if  (time1.hour == 0)  :
                                while True:
                                    time2 = mt5.symbol_info_tick(symbol).time
                                    time1 = (datetime.fromtimestamp(mt5.symbol_info_tick(symbol).time) - timedelta(hours=3))
                                    if (time2 % (3600*4)  < 50) or (time2 % (3600 *4)  < 1200) or (time2 % (3600 *4)  < 600) :
                                        for script_name, args in script_args.items():
                                            # create_file(script_name)  # Create a file for each script
                                            symbol = args[0]
                                            logger = logging.getLogger(symbol)
                                            logger.debug(f'AT the next Hour InTime -- SymbolName : {symbol} BrokerTime : {time1}')
                                            thread = threading.Thread(target=run_script, args=(script_name, *args))
                                            thread.start()

                                        time.sleep(1400)
                                        break
                                    elif time1.hour >= 1:
                                         break

                        
                else:
                    MainLogger.debug("Mt5 Terminal Got Disconnected...")
                    
                    time1 = (datetime.now())
                    with open(f'NotInitial.txt' , 'a') as file:
                                file.write(f'\n symbol = {symbol},')
                                
                                file.write(f'Time = {time1}')
                    file.close
                    cd = mt5.initialize(login = login , password = password, server = server)
                    MainLogger.debug(f'Is Connected : {cd}')



if __name__ == "__main__":
    PreMain()







    
    






