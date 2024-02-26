

def entry_signal1(data,choice,index):
    index = index
    
    # close[4] > low[6]; open[0] <= open[3]; ValueLow(5)[4] > ValueLow(5)[5]; ValueHigh(5)[0] <= ValueClose(5)[4]; ValueHigh(5)[3] <= ValueClose(5)[5]; ValueLow(5)[0] <= ValueClose(5)[1]
    # TimeFrame = H4 , Type = Short
    # Instruments = USDCAD
    if choice == 0:
        condition = True
    
    # close[4] > low[6]; open[0] <= open[3]; ValueLow(5)[4] > ValueLow(5)[5]; ValueHigh(5)[0] <= ValueClose(5)[4]; ValueHigh(5)[3] <= ValueClose(5)[5]; ValueLow(5)[0] <= ValueClose(5)[1]
    # TimeFrame = H4 , Type = Short
    # Instruments = USDCAD
    if choice == 1:
        condition = (data.iloc[index-4]['close'] > data.iloc[index-6]['low']) and \
                    (data.iloc[index-0]['open'] <= data.iloc[index-3]['open']) and \
                    (data.iloc[index-4]['ValueLow'] > data.iloc[index-5]['ValueLow']) and \
                    (data.iloc[index-0]['ValueHigh'] <= data.iloc[index-4]['ValueClose']) and \
                    (data.iloc[index-3]['ValueHigh'] <= data.iloc[index-5]['ValueClose']) and \
                    (data.iloc[index-0]['ValueLow'] <= data.iloc[index-1]['ValueClose']) 
        
    

        
    # low[1] > close[7]; close[4] > high[9]; low[1] <= low[3]; open[1] <= open[4]; ValueOpen(5)[1] <= ValueOpen(5)[4]; CompositeRSI(2;24)[0] >= 10
    # TimeFrame = H4 , Type = Long
    # Instruments = EURUSD
    elif choice == 2:
        condition = (data.iloc[index-1]['low'] > data.iloc[index-7]['close']) and \
                    (data.iloc[index-4]['close'] > data.iloc[index-9]['high']) and \
                    (data.iloc[index-1]['low'] <= data.iloc[index-3]['low']) and \
                    (data.iloc[index-1]['open'] <= data.iloc[index-4]['open']) and \
                    (data.iloc[index-1]['ValueOpen'] <= data.iloc[index-4]['ValueOpen']) and \
                    (data.iloc[index-0]['CompositeRSI_2_24'] >= 10) 
        
        
        
        
        
    # ValueOpen(5)[1] > ValueLow(5)[3]; ValueClose(5)[0] <= ValueLow(5)[1]; AvgTrueRange(10)[0] <= AvgTrueRange(10)[5]; CompositeRSI(2;24)[0] >= 30; rsi(close;2)[0] >= 10; rateOfChange(close;10)[0] > rateOfChange(close;10)[4]
    # TimeFrame = H4 , Type = Long
    # Instruments = GBPUSD
    elif choice == 3:
        condition = (data.iloc[index-1]['ValueOpen'] > data.iloc[index-3]['ValueLow']) and \
                    (data.iloc[index-0]['ValueClose'] <= data.iloc[index-1]['ValueLow']) and \
                    (data.iloc[index-0]['AvgTrueRange_10'] <= data.iloc[index-5]['AvgTrueRange_10']) and \
                    (data.iloc[index-0]['CompositeRSI'] >= 30) and \
                    (data.iloc[index-0]['rsi_2'] >= 10) and \
                    (data.iloc[index-0]['rateOfChange_close_10'] > data.iloc[index-4]['rateOfChange_close_10']) 
        
        
        
    # high[8] > high[9]; low[3] <= low[7]; ValueHigh(5)[0] > ValueLow(5)[2]; ValueLow(5)[2] <= ValueClose(5)[5]; close[0] >= CompositeSMA(8;20;50;200)[0]; CompositeSMA(8;20;50;200)[0] > CompositeSMA(8;20;50;200)[2]
    # TimeFrame = H4 , Type = Long
    # Instruments = USDJPY
    elif choice == 4:
        condition = (data.iloc[index-8]['high'] > data.iloc[index-9]['high']) and \
                    (data.iloc[index-3]['low'] <= data.iloc[index-7]['low']) and \
                    (data.iloc[index-0]['ValueHigh'] > data.iloc[index-2]['ValueLow']) and \
                    (data.iloc[index-2]['ValueLow'] <= data.iloc[index-5]['ValueClose']) and \
                    (data.iloc[index-0]['close'] >= data.iloc[index-0]['CompositeSMA']) and \
                    (data.iloc[index-0]['CompositeSMA'] > data.iloc[index-2]['CompositeSMA']) 
                    
                    
                    
                    
    # open[0] <= high[1]; low[2] <= low[8]; low[3] <= open[5]; close[3] <= low[6]; rsi(close;2)[0] crosses below 40; CompositeEMA(8;20;50;200)[0] <= CompositeEMA(8;20;50;200)[2]
    # TimeFrame = H4 , Type = Long
    # Instruments = US500
    elif choice == 5:
        condition = (data.iloc[index-0]['open'] <= data.iloc[index-1]['high']) and \
                    (data.iloc[index-2]['low'] <= data.iloc[index-8]['low']) and \
                    (data.iloc[index-3]['low'] <= data.iloc[index-5]['open']) and \
                    (data.iloc[index-3]['close'] <= data.iloc[index-6]['low']) and \
                    (data.iloc[index-1]['rsi_2'] > 40 and data.iloc[index-0]['rsi_2'] < 40) and \
                    (data.iloc[index-0]['CompositeEMA'] <= data.iloc[index-2]['CompositeEMA'])   # Crosses Below COndition
        
        
        
        
        
    # high[0] > close[2]; low[1] <= open[2]; high[2] <= open[9]; close[0] < CubeHLC[0]; ValueLow(5)[0] <= 10; ValueClose(5)[1] <= ValueClose(5)[5]
    # TimeFrame = H4 , Type = Long
    # Instruments = US500
    elif choice == 6:
        condition = (data.iloc[index-0]['high'] > data.iloc[index-2]['close']) and \
                    (data.iloc[index-1]['low'] <= data.iloc[index-2]['open']) and \
                    (data.iloc[index-2]['high'] <= data.iloc[index-9]['open']) and \
                    (data.iloc[index-0]['close'] < data.iloc[index-0]['CubeHLC']) and \
                    (data.iloc[index-0]['ValueLow'] <= 10 ) and \
                    (data.iloc[index-1]['ValueClose'] <= data.iloc[index-5]['ValueClose']) 
        
        
        
        
    # open[5] > open[7]; low[0] <= open[2]; close[1] <= close[4]; low[1] <= low[8]; ValueOpen(5)[0] > ValueLow(5)[2]; ValueHigh(5)[2] > ValueOpen(5)[4]
    # TimeFrame = H4 , Type = Long
    # Instruments = US500
    elif choice == 7:
        condition = (data.iloc[index-5]['open'] > data.iloc[index-7]['open']) and \
                    (data.iloc[index-0]['low'] <= data.iloc[index-2]['open']) and \
                    (data.iloc[index-1]['close'] <= data.iloc[index-4]['close']) and \
                    (data.iloc[index-1]['low'] <= data.iloc[index-8]['low']) and \
                    (data.iloc[index-0]['ValueOpen'] > data.iloc[index-2]['ValueLow']) and \
                    (data.iloc[index-2]['ValueHigh'] > data.iloc[index-4]['ValueOpen']) 
        
                    
                    
   
                    
    # high[0] > open[2]; low[6] > low[9]; close[1] <= high[5]; pivotpoint[0] <= pivotpoint[1]; ValueOpen(5)[0] > ValueOpen(5)[1]; momentum(close;5)[0] < momentum(close;5)[1]
    # TimeFrame = H4 , Type = Long
    # Instruments = US30
    elif choice == 8:
        condition = (data.iloc[index-0]['high'] > data.iloc[index-2]['open']) and \
                    (data.iloc[index-6]['low'] > data.iloc[index-9]['low']) and \
                    (data.iloc[index-1]['close'] <= data.iloc[index-5]['high']) and \
                    (data.iloc[index-0]['PivotPoint'] <= data.iloc[index-1]['PivotPoint']) and \
                    (data.iloc[index-0]['ValueOpen'] > data.iloc[index-1]['ValueOpen']) and \
                    (data.iloc[index-0]['momentum_close_5'] < data.iloc[index-1]['momentum_close_5']) 
        
        
        
    #TODO:
    # open[3] > low[5]; low[4] <= close[8]; high[7] <= high[8]; ValueOpen(5)[0] > -6; ValueLow(5)[0] <= ValueLow(5)[5]; high[0] > SMA(close;10)[0]
    # TimeFrame = H4 , Type = Long
    # Instruments = US30
    elif choice == 9:
        condition = (data.iloc[index-3]['open'] > data.iloc[index-5]['low']) and \
                    (data.iloc[index-4]['low'] <= data.iloc[index-8]['close']) and \
                    (data.iloc[index-7]['high'] <= data.iloc[index-8]['high']) and \
                    (data.iloc[index-0]['ValueOpen'] > -6) and \
                    (data.iloc[index-0]['ValueLow'] <= data.iloc[index-5]['ValueLow']) and \
                    (data.iloc[index-0]['high'] > data.iloc[index-0]['sma_10']) 
        
        
        
        
        
    # high[1] > open[4]; close[0] <= low[7]; low[2] <= open[6]; close[4] <= open[9]; close[6] <= high[9]; ADX(20)[0] <= 25
    # TimeFrame = H4 , Type = Long
    # Instruments = US30
    elif choice == 10:
        condition = (data.iloc[index-1]['high'] > data.iloc[index-4]['open']) and \
                    (data.iloc[index-0]['close'] <= data.iloc[index-7]['low']) and \
                    (data.iloc[index-2]['low'] <= data.iloc[index-6]['open']) and \
                    (data.iloc[index-4]['close'] <= data.iloc[index-9]['open']) and \
                    (data.iloc[index-6]['close'] <= data.iloc[index-9]['high']) and \
                    (data.iloc[index-0]['adx_20'] <= 25 ) 
       
                    
                    
                    
        
        
        
        
    # close[3] > open[3]; open[3] > EMA(close;3)[0]; ADX(13)[1] > 9; ADX(10)[10] > 13; ADX(4)[3] > ADX(12)[2]; ADX(9)[4] > ADX(15)[1]
    # TimeFrame = H4 , Type = Long
    # Instruments = US500
    elif choice == 11:
        condition = (data.iloc[index-3]['close'] > data.iloc[index-3]['open']) and \
                    (data.iloc[index-3]['open'] > data.iloc[index-0]['ema_3']) and \
                    (data.iloc[index-1]['adx_13'] > 9) and \
                    (data.iloc[index-10]['adx_10'] > 13) and \
                    (data.iloc[index-3]['adx_4'] > data.iloc[index-2]['adx_2']) and \
                    (data.iloc[index-4]['adx_9'] > data.iloc[index-1]['adx_15']) 
       
                    
                    
                    
                        
    # open[10] > EMA(close;2)[10]; ADX(18)[2] > 1; ADX(6)[7] > 11; ADX(4)[1] > ADX(14)[1]; ADX(5)[4] > ADX(8)[7]; ADX(4)[10] > ADX(5)[6]
    # TimeFrame = H4 , Type = Long
    # Instruments = US500
    elif choice == 12:
        condition = (data.iloc[index-10]['open'] > data.iloc[index-10]['ema_2']) and \
                    (data.iloc[index-2]['adx_18'] > 1) and \
                    (data.iloc[index-7]['adx_6'] > 11) and \
                    (data.iloc[index-1]['adx_4'] > data.iloc[index-1]['adx_14']) and \
                    (data.iloc[index-4]['adx_5'] > data.iloc[index-7]['adx_8']) and \
                    (data.iloc[index-10]['adx_4'] > data.iloc[index-6]['adx_5']) 
        
        
        
        
    # close[3] > EMA(close;1)[0]; ADX(7)[0] > ADX(7)[5]; ADX(10)[2] > ADX(17)[7]; ADX(3)[2] > ADX(10)[9]; ADX(1)[6] > ADX(10)[1]; ADX(5)[6] > ADX(11)[2]
    # TimeFrame = H4 , Type = Long
    # Instruments = US500
    elif choice == 13:
        condition = (data.iloc[index-3]['close'] > data.iloc[index-0]['ema_1']) and \
                    (data.iloc[index-0]['adx_7'] > data.iloc[index-5]['adx_7']) and \
                    (data.iloc[index-2]['adx_10'] > data.iloc[index-7]['adx_17']) and \
                    (data.iloc[index-2]['adx_3'] > data.iloc[index-9]['adx_10']) and \
                    (data.iloc[index-6]['adx_1'] > data.iloc[index-1]['adx_10']) and \
                    (data.iloc[index-6]['adx_5'] > data.iloc[index-2]['adx_11']) 
        
        
        
        
        
    # open[9] < EMA(close;2)[10]; ADX(2)[0] > ADX(17)[4]; ADX(8)[2] > ADX(9)[9]; ADX(3)[4] > ADX(9)[7]; ADX(11)[7] > ADX(16)[5]; ADX(1)[8] > ADX(2)[3]
    # TimeFrame = H4 , Type = Long
    # Instruments = US500
    elif choice == 14:
        condition = (data.iloc[index-9]['open'] < data.iloc[index-10]['ema_2']) and \
                    (data.iloc[index-0]['adx_2'] > data.iloc[index-4]['adx_17']) and \
                    (data.iloc[index-2]['adx_8'] > data.iloc[index-9]['adx_9']) and \
                    (data.iloc[index-4]['adx_3'] > data.iloc[index-7]['adx_9']) and \
                    (data.iloc[index-7]['adx_11'] > data.iloc[index-5]['adx_16']) and \
                    (data.iloc[index-8]['adx_1'] > data.iloc[index-3]['adx_2']) 
        
        
        
        
    # high[0] > low[7]; high[2] > open[4]; low[3] <= open[5]; close[4] <= open[6]; ValueOpen(5)[1] > ValueClose(5)[5]; ValueClose(5)[3] <= ValueOpen(5)[4]
    # TimeFrame = H4 , Type = Short
    # Instruments = GBPUSD
    elif choice == 15:
        condition = (data.iloc[index-0]['high'] > data.iloc[index-7]['low']) and \
                    (data.iloc[index-2]['high'] > data.iloc[index-4]['open']) and \
                    (data.iloc[index-3]['low'] <= data.iloc[index-5]['open']) and \
                    (data.iloc[index-4]['close'] <= data.iloc[index-6]['open']) and \
                    (data.iloc[index-1]['ValueOpen'] > data.iloc[index-5]['ValueClose']) and \
                    (data.iloc[index-3]['ValueClose'] <= data.iloc[index-4]['ValueOpen']) 
        
                    
                    
                    
                    
    # low[0] > open[6]; open[0] > close[2]; low[1] > close[5]; high[8] > close[9]; low[7] <= open[9]; CompositeATR(2;24)[0] > CompositeATR(2;24)[2]
    # TimeFrame = H4 , Type = Short
    # Instruments = GBPUSD
    elif choice == 16:
        condition = (data.iloc[index-0]['low'] > data.iloc[index-6]['open']) and \
                    (data.iloc[index-0]['open'] > data.iloc[index-2]['close']) and \
                    (data.iloc[index-1]['low'] > data.iloc[index-5]['close']) and \
                    (data.iloc[index-8]['high'] > data.iloc[index-9]['close']) and \
                    (data.iloc[index-7]['low'] <= data.iloc[index-9]['open']) and \
                    (data.iloc[index-0]['CompositeATR_2_24'] > data.iloc[index-2]['CompositeATR_2_24']) 
        
        
        
        
    # high[2] > close[9]; low[5] > open[9]; open[6] > close[8]; low[4] <= high[8]; ValueHigh(5)[0] <= ValueOpen(5)[5]; WinsLast(close;5)[0] >= 1
    # TimeFrame = H4 , Type = Short
    # Instruments = EURUSD
    elif choice == 17:
        condition = (data.iloc[index-2]['high'] > data.iloc[index-9]['close']) and \
                    (data.iloc[index-5]['low'] > data.iloc[index-9]['open']) and \
                    (data.iloc[index-6]['open'] > data.iloc[index-8]['close']) and \
                    (data.iloc[index-4]['low'] <= data.iloc[index-8]['high']) and \
                    (data.iloc[index-0]['ValueHigh'] <= data.iloc[index-5]['ValueOpen']) and \
                    (data.iloc[index-0]['WinsLast'] >= 1) 
        
        
        
        
        
    # ADX(5)[4] > ADX(3)[1]; ADX(13)[4] > ADX(9)[10]; ADX(14)[5] > ADX(19)[3]; ADX(18)[6] > ADX(17)[9]; ADX(7)[7] > ADX(19)[7]; ADX(2)[9] > ADX(20)[4]
    # TimeFrame = H4 , Type = Short
    # Instruments = NZDUSD
    elif choice == 18:
        condition = (data.iloc[index-5]['adx_4'] > data.iloc[index-1]['adx_3']) and \
                    (data.iloc[index-4]['adx_13'] > data.iloc[index-10]['adx_9']) and \
                    (data.iloc[index-5]['adx_14'] > data.iloc[index-3]['adx_19']) and \
                    (data.iloc[index-6]['adx_18'] > data.iloc[index-9]['adx_17']) and \
                    (data.iloc[index-7]['adx_7'] > data.iloc[index-7]['adx_19']) and \
                    (data.iloc[index-9]['adx_2'] > data.iloc[index-4]['adx_20']) 
        
        
        
      
      

        
    else:
        condition =  False

    if condition:
        return True
    else:
        return False