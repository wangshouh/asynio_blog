import asyncio
import time

limit = asyncio.Semaphore(2)

async def hello(name: int):
    async with limit:
        await asyncio.sleep(1)
    print(f"{name} Finish...")

async def main():
    task = [hello(i) for i in range(6)]
    await asyncio.gather(*task)


s = time.perf_counter()
asyncio.run(main())
elapsed = time.perf_counter() - s
print(f"Code runtime: {elapsed}")