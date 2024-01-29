import MetaTrader5 as mt5
login = 25088141
password = 'N3W*f%Ts??kF'
server = 'Tickmill-Demo'
path = r'C:\Program Files\MetaTrader 5\terminal64.exe'
mt5.initialize( login = login , password = password, server = server)


from datetime import datetime , timedelta

time1 = (datetime.fromtimestamp(mt5.symbol_info_tick('EURUSD').time) - timedelta(hours=1))

print(time1)