import asyncio
import multiprocessing
import re
import time
from concurrent.futures import ProcessPoolExecutor, wait
from multiprocessing import Queue

import aiohttp
from aiohttp import ClientSession


def exact_link(html: str, pattern: re.Pattern):
    return re.search(pattern, html).group(1)


def consumer(rx: Queue, pattern: re.Pattern):
    while True:
        html = rx.get()

        if html is None:
            break

        title = exact_link(html, pattern)
        print(title)



async def run_loop(tx: Queue, rx: Queue):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.5,zh-TW;q=0.3,zh-HK;q=0.2',
    }
    # pending = set()
    async with ClientSession(headers=headers) as session:
        while True:
            task = tx.get_nowait()
            fn, args = task
            future_task = asyncio.create_task(fn(*args, session))
            res = await future_task
            rx.put_nowait(res)


def bootstrap(tx: Queue, rx: Queue):
    asyncio.run(run_loop(tx, rx))


def consumer(rx: Queue, pattern: re.Pattern):
    while True:
        html = rx.get()
        title = exact_link(html, pattern)
        print(title)


def main():
    num_producers = 2

    pattern = re.compile(r"<title>(.*)</title>")
    with open(r"test_data\url_list", "r", encoding="utf-8") as f:
        url_list = f.readlines()

    with multiprocessing.Manager() as manager:
        tx, rx = manager.Queue(), manager.Queue()

        for url in url_list:
            task = fetch_url, (url,)
            tx.put_nowait(task)

        with ProcessPoolExecutor(max_workers=4) as executor:
            producers = [executor.submit(bootstrap, tx, rx) for _ in range(2)]
            consumers = [executor.submit(consumer, rx, pattern) for _ in range(2)]
            wait(producers)
            rx.put(None)
            rx.put(None)


if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"Code runtime: {elapsed}")
