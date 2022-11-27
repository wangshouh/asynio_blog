import requests
import time
import asyncio
import aiohttp
from aiohttp import ClientSession


def get_api():
    url = "https://mocki.io/v1/d4867d8b-b5d5-4a48-a4ab-79131b5809b8"
    req = requests.get(url).json()
    print(req)


def main():
    for i in range(3):
        get_api()


async def aio_get_api(session: ClientSession):
    url = "https://mocki.io/v1/d4867d8b-b5d5-4a48-a4ab-79131b5809b8"
    req = await session.get(url)
    
    print(await req.json())


async def aio_main():
    async with ClientSession() as session:
        task = [aio_get_api(session) for _ in range(3)]
        await asyncio.gather(*task)

if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(aio_main())
    # main()
    elapsed = time.perf_counter() - s
    print(f"Code runtime: {elapsed}")
