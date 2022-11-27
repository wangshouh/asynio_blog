import asyncio


async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")


async def main():
    async with asyncio.TaskGroup() as tg:
        for i in range(3):
            tg.create_task(count())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"Code runtime: {elapsed:.2f}")
