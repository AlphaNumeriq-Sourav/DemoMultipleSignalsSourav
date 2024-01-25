

def entry_signal1(data,choice,index):
    index = index
    
    # high[2] > close[9]; low[5] > open[9]; open[6] > close[8]; low[4] <= high[8]; ValueHigh(5)[0] <= ValueOpen(5)[5]; WinsLast(close;5)[0] >= 1
    # TimeFrame = H4 , Type = Short
    # Instruments = EURUSD 
    if choice == 1:
        condition = (data.iloc[index-2]['high'] > data.iloc[index-9]['close']) and \
                    (data.iloc[index-5]['low'] > data.iloc[index-9]['open']) and \
                    (data.iloc[index-6]['open'] > data.iloc[index-8]['close']) and \
                    (data.iloc[index-4]['low'] <= data.iloc[index-8]['high'] ) and \
                    (data.iloc[index-0]['ValueHigh'] <= data.iloc[index-5]['ValueOpen']) and \
                    (data.iloc[index-0]['WinsLast'] >= 1)
                    
                    
    
    elif choice == 2:
        condition = (data.iloc[index-1]['rsi_14'] > 1)
        
        
        
    # high[0] > low[7]; high[2] > open[4]; low[3] <= open[5]; close[4] <= open[6]; ValueOpen(5)[1] > ValueClose(5)[5]; ValueClose(5)[3] <= ValueOpen(5)[4]
    # TimeFrame = H4 , Type = Short
    # Instruments = GBPUSD
    elif choice == 3:
        condition = (data.iloc[index-0]['high'] > data.iloc[index-7]['low']) and \
                    (data.iloc[index-2]['high'] > data.iloc[index-4]['open']) and \
                    (data.iloc[index-3]['low'] <= data.iloc[index-5]['open']) and \
                    (data.iloc[index-4]['close'] <= data.iloc[index-6]['open']) and \
                    (data.iloc[index-1]['ValueOpen'] > data.iloc[index-5]['ValueClose']) and \
                    (data.iloc[index-3]['ValueClose'] <= data.iloc[index-4]['ValueOpen']) 
        variable = "Trail"
        
        
        
        
    # low[0] > open[6]; open[0] > close[2]; low[1] > close[5]; high[8] > close[9]; low[7] <= open[9]; CompositeATR(2;24)[0] > CompositeATR(2;24)[2]
    # TimeFrame = H4 , Type = Short
    # Instruments = GBPUSD
    elif choice == 4:
        condition = (data.iloc[index-0]['low'] > data.iloc[index-6]['open']) and \
                    (data.iloc[index-0]['open'] > data.iloc[index-2]['close']) and \
                    (data.iloc[index-1]['low'] > data.iloc[index-5]['close']) and \
                    (data.iloc[index-8]['high'] > data.iloc[index-9]['close']) and \
                    (data.iloc[index-7]['low'] <= data.iloc[index-9]['open']) and \
                    (data.iloc[index-0]['CompositeATR_2_24'] > data.iloc[index-2]['CompositeATR_2_24']) 
        variable = "Trail"
        
        
    # ADX(5)[4] > ADX(3)[1]; ADX(13)[4] > ADX(9)[10]; ADX(14)[5] > ADX(19)[3]; ADX(18)[6] > ADX(17)[9]; ADX(7)[7] > ADX(19)[7]; ADX(2)[9] > ADX(20)[4]
    # TimeFrame = H4 , Type = Short
    # Instruments = NZDUSD
    elif choice == 5:
        '''
        '''
        condition = (data.iloc[index-4]['adx_5'] > data.iloc[index-1]['adx_3']) and \
                    (data.iloc[index-4]['adx_13'] > data.iloc[index-10]['adx_9']) and \
                    (data.iloc[index-5]['adx_14'] > data.iloc[index-3]['adx_19']) and \
                    (data.iloc[index-6]['adx_18'] > data.iloc[index-9]['adx_17']) and \
                    (data.iloc[index-7]['adx_7'] > data.iloc[index-7]['adx_19']) and \
                    (data.iloc[index-9]['adx_2'] > data.iloc[index-4]['adx_20']) 
        
        
        
        
    # open[10] > EMA(close;2)[10]; ADX(10)[0] > ADX(19)[5]; ADX(2)[3] > ADX(2)[9]; ADX(15)[10] > ADX(20)[4]; ADX(2)[10] > ADX(15)[5]; ADX(1)[10] > ADX(7)[9]
    # TimeFrame = H4 , Type = Short 
    # Instruments = US500
    # elif choice == 5:
    #     condition = (data.iloc[index-10]['open'] > data.iloc[index-9]['ema_2']) and \
    #                 (data.iloc[index-0]['adx_10'] > data.iloc[index-5]['adx_19']) and \
    #                 (data.iloc[index-3]['adx_2'] > data.iloc[index-9]['adx_2']) and \
    #                 (data.iloc[index-10]['adx_15'] > data.iloc[index-4]['adx_20'] ) and \
    #                 (data.iloc[index-10]['adx_2'] > data.iloc[index-5]['adx_15']) and \
    #                 (data.iloc[index-10]['adx_1'] > data.iloc[index-9]['adx_7'])
        
    
    
    # close[7] < SMA(close;2)[8]; open[8] > EMA(close;3)[8]; ADX(1)[1] > ADX(20)[1]; ADX(3)[3] > ADX(9)[9]; ADX(7)[9] > ADX(11)[0]; ADX(3)[9] > ADX(13)[3]
    # open[10] > close[10]; high[0] > SMA(close;3)[0]; ADX(9)[0] > ADX(9)[7]; ADX(13)[1] > ADX(16)[1]; ADX(3)[6] > ADX(20)[9]; ADX(8)[10] > ADX(19)[4]
    # open[10] > open[9]; ADX(16)[0] > ADX(16)[4]; ADX(3)[2] > ADX(8)[0]; ADX(3)[4] > ADX(20)[0]; ADX(2)[9] > ADX(18)[5]; ADX(20)[0] <= ADX(11)[0]
    # ADX(19)[0] > 15; ADX(6)[9] > 5; ADX(2)[0] > ADX(16)[1]; ADX(3)[0] > ADX(15)[3]; ADX(3)[1] > ADX(2)[8]; ADX(6)[9] > ADX(19)[3]

        
    else:
        condition =  False

    if condition:
        return True
    else:
        return False