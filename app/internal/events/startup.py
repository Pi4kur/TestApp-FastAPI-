import os
from app.internal.schemas.currency import Symbols
from app.pkg.redis_tools.tools import RedisTools

import aiohttp

async def on_startup():
    async with aiohttp.ClientSession() as session:

        async with session.get(os.getenv('ALL_PAIRS_KEY')) as resp:
            resp_json = await resp.json()
            
            parsed_pairs = Symbols(**resp_json)
            
            cutted_pairs = parsed_pairs.symbols[:20]
            
            symbols = [pair.symbol for pair in cutted_pairs]
            
            for symbol in symbols:
                RedisTools.set_pair(symbol, 0)