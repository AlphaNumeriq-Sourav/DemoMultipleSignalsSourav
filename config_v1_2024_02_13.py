
# SymbolName, RISK, TPInPipets, SLInPipets, TrailTPPointsInPipets ,SLTrailFirstSLPointInPipets, RiskModel_SerialNo, RiskModelName,EntryType

# thread_H4_Jan24_Signal_EURUSD_GBPUSD_NZDUSD_BySourav = {
#         "Short_H4_1" : ('GBPUSD' , 1/100  , 300 , 500 , 10 ,100, [0] , ['Trail'], "Long"),
#         "Short_H4_2" : ('USDJPY' , 1/100  , 300 , 500 , 10, 100, [0] , ['Trail'], "Long"),
#         "Short_H4_3" : ('AUDCAD' , 1/100 , 300 , 500  , 10, 100, [0] , ['Trail'], "Short") ,
#         "Short_H4_4" : ('NZDUSD' , 1/100 , 300 , 500 , 10 , 100 , [0] , ['Trail'], "Short") ,
#         "Short_H4_5" : ('XAUUSD' , 1/100 , 30 , 50 , 1, 10, [0] , ['ATR'], "Short"),
#         "Short_H4_6" : ('US30' , 1/100 , 3000 , 5000 , 10, 100, [0] , ['SL_Trail'], "Short"),
#         "Short_H4_7" : ('XTIUSD' , 1/100 , 3000 , 5000 ,10 , 100,[0] , ['ATR'], "Short") ,
#         "Short_H4_8" : ('US500' , 1/100 , 3000 , 5000 , 10 , 100,[0] , ['SL_Trail'], "Long") 
#     }

thread_H4_Jan24_Signal_EURUSD_GBPUSD_NZDUSD_BySourav = {
        "Short_H4_1" : ('USDCAD' , 1/100  , 300 , 500 , 10 ,100, [1] , ['ATR'], "Short"),
        "Short_H4_2" : ('EURUSD' , 1/100 , 300 , 500 , 10, 100, [2] , ['ATR'], "Long"),
        "Short_H4_3" : ('GBPUSD' , 1/100 , 300 , 500 , 10, 100, [3] , ['Trail'], "Long"),
        "Short_H4_4" : ('USDJPY' , 1/100 , 300 , 500 ,10 , 100,[4] , ['Trail'], "Long") ,
        "Short_H4_5" : ('US500' , 1/100 , 30 , 50 ,1 , 10, [5,6,7,11,12,13,14] , ['SL_Trail', 'SL_Trail', 'SL_Trail', 'SL_Trail', 'SL_Trail', 'SL_Trail', 'SL_Trail'], "Long") ,
        "Short_H4_6" : ('US30' , 1/100 , 30 , 50 ,1 , 10, [8,9,10] , ['SL_Trail', 'SL_Trail', 'SL_Trail'], "Long") ,
        "Short_H4_7" : ('GBPUSD' , 1/100 , 300 , 500 ,10 , 100, [15,16] , ['Trail' , 'Trail'], "Short") ,
        "Short_H4_8" : ('EURUSD' , 1/100 , 300 , 500 ,10 , 100, [17] , ['Trail'], "Short") ,
        "Short_H4_9" : ('NZDUSD' , 1/100 , 300 , 500 ,10 , 100, [18] , ['Trail'], "Short") 
    }

SkipTrades = False
# 15 , 16 , 2,3,17

