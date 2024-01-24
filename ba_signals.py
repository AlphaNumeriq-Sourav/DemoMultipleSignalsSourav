

def entry_signal1(data,choice,index):
    index = index
    '''
    high[2] > close[9]; low[5] > open[9]; open[6] > close[8]; low[4] <= high[8]; ValueHigh(5)[0] <= ValueOpen(5)[5]; 
    WinsLast(close;5)[0] >= 1
    '''
    
    if choice == 1:
        condition = (data.iloc[index-2]['high'] > data.iloc[index-9]['close']) and \
                    (data.iloc[index-5]['low'] > data.iloc[index-9]['open']) and \
                    (data.iloc[index-6]['open'] > data.iloc[index-8]['close']) and \
                    (data.iloc[index-4]['low'] <= data.iloc[index-8]['high'] ) and \
                    (data.iloc[index-0]['ValueHigh'] <= data.iloc[index-5]['ValueOpen']) and \
                    (data.iloc[index-0]['WinsLast'] >= 1)
                    
        
        
    elif choice == 2:
        condition = (data.iloc[index-1]['rsi_14'] > 1)
        
    else:
        condition =  False

    if condition:
        return True
    else:
        return False