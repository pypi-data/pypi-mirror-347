import asyncio
from aiohttp import ClientSession


async def __is_valid_proxy(proxy:str, url:str, timeout:int, session: ClientSession) -> tuple[bool, str]:
    try:
        async with session.get(url=url,
                               proxy=proxy,
                               timeout=timeout) as response:
            return True, proxy

    except Exception:
        return False, proxy


async def check_proxies(proxy_list:list, url:str, timeout: int=10):
    async with ClientSession() as session:
        tasks = [__is_valid_proxy(proxy=proxy,
                                  url=url,
                                  timeout=timeout,
                                  session=session) for proxy in proxy_list]

        result = await asyncio.gather(*tasks)

        return result