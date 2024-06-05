#%%
import asyncio
import websockets
import json
import nest_asyncio
nest_asyncio.apply()
import pandas as pd
#%%
msg = \
{
  "jsonrpc" : "2.0",
  "id" : 9290,
  "method" : "public/get_last_trades_by_currency",
  "params" : {
    "currency" : "BTC",
    "kind": "option",
    "sorting":"desc",
    "start_timestamp":1697249784000,
    "end_timestamp": 1697271619520,
    "count": 1000
  }
}

async def call_api(msg):
   async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
       await websocket.send(msg)
       while websocket.open:
           response = await websocket.recv()
           # do something with the response...
           return response

res = asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))
#%%
json_object = json.loads(res)
#%%
trades_df = pd.json_normalize(json_object['result']['trades'])


# %%
