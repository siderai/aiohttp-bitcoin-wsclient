import asyncio
from typing import List

import aiohttp


URL = 'wss://ws.bitmex.com/realtime'
BITMEX_COMMAND = {"op":"subscribe","args":["instrument:XBTUSD"]}
FIELD_SELECTED = 'fairPrice'

async def fetch_10() -> List[float]:
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(URL) as ws:
            await _perform_request(ws)
            return await _parse_messages(ws)


async def _perform_request(ws):
    await ws.send_json(BITMEX_COMMAND)

    
async def _parse_messages(ws):
    results = []
    counter = 0
    
    async for msg in ws:        
        if counter >= 10:
            return results

        if msg.type == aiohttp.WSMsgType.TEXT:
            if FIELD_SELECTED in msg.data:
                message_dict = msg.json()
                data: List[dict] = message_dict['data']
                for dict_ in data:
                    value = dict_[f'{FIELD_SELECTED}']
                    results.append(value)
                    print(value)
                    counter += 1

        elif msg.type in (aiohttp.WSMsgType.CLOSED,
                          aiohttp.WSMsgType.ERROR):
            print('Connection error! Exiting')
            raise SystemExit(0)


if __name__ == '__main__':
    asyncio.run(fetch_10())
