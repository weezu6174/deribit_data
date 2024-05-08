#%%
import asyncio
import websockets
import pandas as pd
import json
import nest_asyncio
nest_asyncio.apply()
import pprint
#%%
msg = \
{
    "jsonrpc": "2.0",
    "id":9344,
    "method":"public/get_book_summary_by_currency",
    "params": {
        "currency": "BTC",
        "kind": "option"
    }
}

async def call_api(msg):
    async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
        await websocket.send(msg)
        while websocket.open:
            response = await websocket.recv()
           # do something with the response...
            return response

res = asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msg)))

#%%
json_object = json.loads(res)
summary_df = pd.json_normalize(json_object['result'])
# %%
