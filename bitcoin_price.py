import websocket
import json
from datetime import datetime

API_KEY = "ccte93iad3i1e17hor4gccte93iad3i1e17hor50"
WEBSOCKET_URL = f"wss://ws.finnhub.io?token={API_KEY}"

# Global dictionary variable that holds the trades for each minute
trades_per_minute = {}
# Global variable that holds the previous minute as datetime object
previous_minute_dt = None

def on_message_all_trades(ws, message):
    '''Parses the message json string and prints the timestamp, price and volume of the trades'''
    trades = json.loads(message)

    for trade in trades['data']:
        dt = datetime.fromtimestamp(int(trade['t']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{dt} price:{trade['p']} volume:{trade['v']}")


def calc_vwa_price(trades):
    '''Calculates Volume Weighted Average Price from a sequence of price and volume values'''

    # Return None if list is empty
    if not trades:
        return None
    
    sum_volume_price = 0.0
    sum_volume = 0.0

    for trade in trades:
        sum_volume_price += (trade['price'] * trade['volume'])
        sum_volume += trade['volume']
        
    vwa_price = sum_volume_price / sum_volume
    return vwa_price

def store_trade(trade):
    '''Stores trade data in a dictionary based on the timestamp'''
    global trades_per_minute

    timestamp_ms = trade['t']
    price = trade['p']
    volume = trade['v']

    # Convert the trade timestamp to datetime rounded down to minute
    trade_timestamp_dt = datetime.fromtimestamp(int(timestamp_ms) / 1000).replace(second=0, microsecond=0)

    # If no entry in the dictionary exist for the trade timestamp, create a new entry with empty list value
    if trade_timestamp_dt not in trades_per_minute:
        trades_per_minute[trade_timestamp_dt] = []

    # Append the price and volume for the trade as dictionary to the list for the corresponding key timestamp
    trades_per_minute[trade_timestamp_dt].append({'price': price, 'volume': volume})

def on_message_vwa_price(ws, message):
    '''Prints the Volume Weighted Average Price for trades for each minute'''
    
    global previous_minute_dt

    trades = json.loads(message)

    for trade in trades['data']:
        
        # Threshold value in seconds which determines how long to wait before calculating the
        # volume weighted average price for the trades from the previous minute.
        # Value is larger than 60 seconds to accomadate late ariving transactions
        threshold = 70

        store_trade(trade)

        # Get current time
        current_time = datetime.now()

        # Check if threshold has been reached
        if previous_minute_dt and (current_time - previous_minute_dt).total_seconds() > threshold:
            
            # Calculate VWAP for the previous minute
            vwa_price = round(calc_vwa_price(trades_per_minute[previous_minute_dt]), 2)
            if vwa_price:
                print(f"Volume Weighted Average Price for {previous_minute_dt.strftime('%H:%M')}-{current_time.strftime('%H:%M')}: {vwa_price}")
            
            # Clear the data for the previous minute
            del trades_per_minute[previous_minute_dt]

            # Update the previous minute to the current one rounded down to minutes
            previous_minute_dt = current_time.replace(second=0, microsecond=0)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

def show_trades():
    '''Creates a websocket to Binance exchange and assigns a message handler that shows all trades.'''
    ws = websocket.WebSocketApp(WEBSOCKET_URL,
                              on_message = on_message_all_trades,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()


def vwa_price():
    '''Creates a websocket to Binance exchange and assigns a message handler that calculates the Volume Weighted Average Price of the trades each minute.'''
    global previous_minute_dt
    
    # Set initial value
    previous_minute_dt = datetime.now().replace(second=0, microsecond=0)

    ws = websocket.WebSocketApp(WEBSOCKET_URL,
                              on_message = on_message_vwa_price,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()


if __name__ == "__main__":

    choice = '0'

    while choice != '1' and choice != '2':
        choice = input('Enter 1 to show all trades or 2 to show Volume Weighted Average Price of the trades each minute: ')

    if choice == '1':
        show_trades()
    else:
        vwa_price()

