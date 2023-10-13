import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


async def call_api(msg):
   async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
       await websocket.send(msg)
       while websocket.open:
           response = await websocket.recv()
           return response



def async_loop(api, message):
    return asyncio.get_event_loop().run_until_complete(api(message))


def retrieve_historic_data(start, end, instrument, timeframe):
    msg = \
        {
            "jsonrpc": "2.0",
            "id": 833,
            "method": "public/get_tradingview_chart_data",
            "params": {
                "instrument_name": instrument,
                "start_timestamp": start,
                "end_timestamp": end,
                "resolution": timeframe
            }
        }
    resp = async_loop(call_api, json.dumps(msg))

    return resp

def json_to_dataframe(json_resp):
    res = json.loads(json_resp)

    df = pd.DataFrame(res['result'])

    df['ticks'] = df.ticks / 1000
    df['timestamp'] = [datetime.fromtimestamp(date) for date in df.ticks]

    return df



if __name__ == '__main__':
    start = 1672534800000
    end = 1680310800000
    instrument = "BTC-30JUN23-30000-C"
    timeframe = '60'

    json_resp = retrieve_historic_data(start, end, instrument, timeframe)

    df = json_to_dataframe(json_resp)
    print(df.head(50))
    plt.plot(df.ticks,df['close'])
    plt.show()
